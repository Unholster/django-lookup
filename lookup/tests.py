# -*- coding: utf8

from django.test import TestCase
from . import LookupTable
from models import Dummy

class LookupTests(TestCase):
    def setUp(self):
        self.dummy1 = Dummy.objects.create(name='The dummy one')
        self.dummy2 = Dummy.objects.create(name="The dummy two")
        self.dummy3 = Dummy.objects.create(name='not even close')
        self.table= LookupTable(Dummy)
        self.table.create_aliases("name")
        self.table.refresh_cache()

    def test_lookup(self):
        attempts = [
            u'The dummy one',
            u'ThEdummYOne',
            u'ThédümmYO\'ne',
            u'The dummi one',
        ]
        for attempt in attempts:
            found = self.table.lookup(attempt)
            self.assertEqual(found, self.dummy1)

    def test_normalize(self):
        attempts = [
            u'The dummy one',
            u'ThEdummYOne',
            u'ThédümmYO\'ne',
            u'The dummi one',
        ]
        for attempt in attempts:
            normalized = self.table.normalize(attempt)
            self.assertEqual(
                    normalized,
                    "thedummione",
                    u"Attempted: %s, got: %s" % (attempt, normalized)
                )

    def test_suggest(self):
        suggestions = self.table.suggestions("the dummy ode")
        self.assertEqual(suggestions.get("thedummione"), self.dummy1, suggestions)
        self.assertEqual(suggestions.get("thedummitwo"), self.dummy2, suggestions)
        self.assertEqual(suggestions.get("thedummiold"), None, suggestions)

    def test_add_alias(self):
        new_alias = 'foo'
        with self.assertRaises(KeyError):
            self.table.lookup(new_alias)
        self.table.add_alias(new_alias, self.dummy1)
        self.assertEqual(
                self.table.lookup(new_alias),
                self.dummy1
            )