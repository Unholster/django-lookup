from .testapp.models import Thing

def ThingFactory():  # noqa
    thing = Thing()
    thing.save()
    return thing
