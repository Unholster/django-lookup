django-lookup
=============
Provides lookup tables for Django models including fuzzy-matching helpers and lookup table management features.

Quick start
-----------

1. Add "lookup" to your `INSTALLED_APPS` :
```python
    INSTALLED_APPS = (
        ...
        'lookup',
    )
```
2. Run `python manage.py syncdb` to create the lookup models
3. Configure a cache backend (not required)
```python
    LOOKUP_CACHE_BACKEND = "redis://localhost"
```
4. Configure domain options (not required)
```python
    LOOKUP_DOMAINS = {
        'stuff': {
            'comparison_function': 'myapp.compare_keys',
        }
    }
```


Usage example
-----
```python
import lookup
from myapp.models import Thing

domain = lookup.Domain("stuff")

def make_key(name):
  return name.lower().split(" ")[0]

name = "Foo bar"
key = key_from_name(name)  # "foo"

try:
  # Lookup a Thing by "foo" in the "stuff" domain
  obj = domain.get(key)
except LookupFailed:
  # Find objects with similar keys (within a 0.25 threshold)
  results = domain.search(key, threshold=0.25)
  if len(results) > 0:
    # Found a close-enough result
    obj, similarity = results
  else:
    # We'll add this Thing since it hasn't been found
    thing = Thing(name=name) # "Foo bar"
    domain.set(key, thing) # foo -> Thing(Foo bar), in stuff domain
```
