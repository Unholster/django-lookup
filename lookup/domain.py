from difflib import SequenceMatcher
import importlib
from django.conf import settings
from django.db import IntegrityError
from .models import Alias


def default_comparison_function(a, b):
    return SequenceMatcher(None, a, b).ratio()


class Domain:
    _configurations = {}

    def __init__(
        self,
        name="",
        comparison_function=None
    ):
        domain_config = Domain._configurations.get(name, {})
        self.name = name
        if comparison_function is None:
            try:
                self.compare = domain_config['compare']
            except KeyError:
                self.compare = default_comparison_function
        else:
            self.compare = comparison_function

    def set(self, key, obj):
        try:
            Alias.objects.create(
                domain=self.name,
                key=key,
                target=obj
            )
        except IntegrityError:
            raise ValueError('Key already exists in this domain')

    def get(self, key):
        try:
            return Alias.objects.get(domain=self.name, key=key).target
        except Alias.DoesNotExist:
            raise KeyError('Key not found in domain')

    def search(self, key, cutoff=0):
        results = []
        for k in self.keys():
            similarity = self.compare(key, k)
            if similarity >= cutoff:
                results.append((k, similarity))
        return sorted(results, key=lambda item: item[1], reverse=True)

    def keys(self):
        return Alias.objects.filter(domain=self.name)\
            .values_list('key', flat=True)

    @staticmethod
    def _configure():
        configs = getattr(settings, 'LOOKUP_DOMAINS', {})
        for name, config in configs.items():
            domain_config = {}
            comp_func_str = config.get('comparison_function')
            if comp_func_str is not None:
                module_name, function_name = comp_func_str.rsplit('.', 1)
                module = importlib.import_module(module_name)
                func = getattr(module, function_name)
                assert callable(func)
                domain_config['compare'] = func

            Domain._configurations[name] = domain_config

Domain._configure()
