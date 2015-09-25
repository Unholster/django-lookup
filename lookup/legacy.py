from django.db import IntegrityError
from .models import Alias, ContentType
from unidecode import unidecode
from difflib import get_close_matches
import re
import collections


STRIP_RE = re.compile(r'[^a-z0-9#]')


def default_normalization(text):
    return STRIP_RE.sub('', unidecode(text.lower().replace("y", "i")))


class LookupCache(dict):
    def __setitem__(self, key, value):
        if value is None:
            raise ValueError('None value not allowed in LookupCache')
        super(LookupCache, self).__setitem__(key, value)


class LookupTable(object):
    def __init__(
        self, modelclass, key_prefix=None, persist=True, filters=None
    ):
        self.model = modelclass
        self.key_prefix = key_prefix
        if type(filters) is dict:
            self.filtered = self.model.objects.filter(**filters)
        elif type(filters) is list:
            self.filtered = self.model.objects.filter(*filters)
        else:
            self.filtered = self.model.objects.all()
        self.persist = persist
        self.clean()
        self.refresh_cache()

    def __iter__(self):
        return iter(self._cache.values())

    def lookup(self, *keys):
        return self._cache[self.normalize(*keys)]

    def clean(self):
        if self.persist:
            for alias in Alias.objects.filter(
                target_type=ContentType.objects.get_for_model(self.model),
            ):
                if alias.target is None:
                    alias.delete()
            self.refresh_cache()

    def refresh_cache(self):
        aliases = Alias.objects.filter(
            target_type=ContentType.objects.get_for_model(self.model),
            target_id__in=self.filtered
        )
        self._cache = LookupCache({a.key: a.target for a in aliases})

    def delete_aliases(self):
        aliases = Alias.objects.filter(
            target_type=ContentType.objects.get_for_model(self.model),
            target_id__in=self.filtered
        )
        aliases.delete()

    def normalize(self, *keys):
        if self.key_prefix is not None:
            keys = (self.key_prefix,) + keys
        text = "#".join([default_normalization(key) for key in keys])
        return text

    def prompt(self, text, lookup=True, create=False, defaults={}, **kwargs):
        obj = None
        created = False

        if lookup:
            try:
                return self.lookup(text), created
            except KeyError:
                pass

        model_label = self.model.__name__.title()

        while not obj:
            print("%s not found for %s <%s>" % (
                model_label, text, self.normalize(text)
            ))
            print("Options:")
            print("  0 - Ignore")
            offset = 1
            suggestions = list(self.suggestions(text, **kwargs).items())
            for i, (key, suggestion) in enumerate(suggestions):
                print("  %d - <%s> %s" % (i + offset, key, suggestion))
            if create:
                print("  c - Create")
                if isinstance(defaults, collections.Callable):
                    defaults = defaults(text)
                create_obj = self.prompt_create(defaults)

            try:
                choice = input("Enter choice:")
            except ValueError:
                print("Unknown option: %d" % choice)
                continue

            if choice == '0':
                raise KeyError
            if choice.lower() == 'c':
                create_obj.save()
                obj = create_obj
                created = True
            else:
                try:
                    key, obj = suggestions[int(choice) - offset]
                except (ValueError, IndexError):
                    print("Unknown option: %s" % choice)

        self.add_alias(text, obj)
        return obj, created

    def prompt_create(self, defaults):
        obj = self.model(**defaults)
        print("******** Create *********")
        for f in self.model._meta.get_all_field_names():
            if hasattr(obj, f):
                print("   %s: %s" % (f, getattr(obj, f)))
        print("*************************")
        return obj

    def create_aliases(self, key_gen=None):
        if key_gen is None and hasattr(self.model, 'keygen'):
            key_gen = self.model.keygen
        elif not isinstance(key_gen, collections.Callable):
            field_name = key_gen
            key_gen = lambda o: getattr(o, field_name)

        for obj in self.filtered:
            try:
                self.add_alias(key_gen(obj), obj)
            except IntegrityError:
                pass

    def add_alias(self, text, target):
        key = self.normalize(text)
        if self.persist:
            Alias.objects.create(
                key=key,
                target=target
            )
        self._cache[key] = target

    def suggestions(self, text, n=3, cutoff=0.5):
        normalized = self.normalize(text)
        matches = get_close_matches(
            normalized, list(self._cache.keys()), n=n, cutoff=cutoff
        )
        return {k: self._cache[k] for k in matches}
