import pytest
from lookup import Domain
from .factories import ThingFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def keyset():
    """
    Creates a set of numeric keys centered around 0
    Provides a comparison function based on numeric closeness of the
    keys
    """

    class KeySet:
        extent = 10

        def __init__(self):
            self.key = "0"
            self.all = [self.key]
            for i in range(KeySet.extent):
                self.all.append(str(i + 1))

        @staticmethod
        def compare(k1, k2):
            return abs(int(k1) - int(k2)) / KeySet.extent

    return KeySet()


def test_get():
    item = ThingFactory()
    domain = Domain()
    domain.set('foo', item)
    assert domain.get('foo').pk == item.pk


def test_search(keyset):
    cutoff = 0.5
    domain = Domain(comparison_function=keyset.compare)

    # Add all except the main key
    # build the expected set along the way
    expected = []
    for k in keyset.all:
        if k != keyset.key:
            thing = ThingFactory()
            domain.set(k, thing)
            similarity = keyset.compare(keyset.key, k)
            if similarity >= cutoff:
                expected.append((k, similarity))
    expected.sort(key=lambda item: item[1], reverse=True)

    result = domain.search(keyset.key, cutoff=cutoff)
    assert list(result) == expected


def test_segregated_get():
    key = "KEY"
    domain1 = Domain("foo")
    domain2 = Domain("bar")
    domain1.set(key, ThingFactory())
    domain2.set(key, ThingFactory())
    assert domain1.get(key) != domain2.get(key)


def test_segregated_search(keyset):
    domain1 = Domain("foo")
    domain2 = Domain("bar")
    for i, k in enumerate(keyset.all[1:]):
        if i % 2 == 0:
            domain1.set(k, ThingFactory())
        else:
            domain2.set(k, ThingFactory())

    key = keyset.key
    assert len(domain1.keys()) > 0
    assert len(domain2.keys()) > 0
    assert len(list(domain1.search(key))) > 0
    assert len(list(domain1.search(key))) == len(list(domain2.search(key)))
    assert list(domain1.search(key)) != list(domain2.search(key))


def test_domain_configuration(settings):
    settings.LOOKUP_DOMAINS = {
        'custom': {
            'comparison_function': 'test.testapp.custom_function',
        }
    }
    Domain._configure()
    from test.testapp import custom_function
    from lookup import default_comparison_function
    domain = Domain('custom')
    assert domain.compare == custom_function

    domain = Domain()
    assert domain.compare == default_comparison_function


def test_unique_keys():
    key = 'KEY'
    domain = Domain()
    domain.set(key, ThingFactory())
    with pytest.raises(ValueError):
        domain.set(key, ThingFactory())
