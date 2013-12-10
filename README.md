django-lookup
=============
Lookup is a simple Django app to easy work with slug charfields and fuzzy finding in
your models.

Quick start
-----------

1. Add "lookup" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'lookup',
    )

2. Run `python manage.py syncdb` to create the lookup models.
            
Use example:
        def option_key(self, option):
        	return option.name if hasattr(option, 'name') else option

		...

		fuzzy_string = "Some incorrectly spelled key"  
  		
  		# Creates a lookup object for the Territory model
    	zone_lookup = LookupTable(Territory)

    	# Creates a lookup list using what's already on the table.
        zone_lookup.create_aliases(self.option_key) 

        # Obtains a territory using a slug from the fuzzy_string and tries to obtain the object associated to it
        # if no exact matches, proposes alternatives using fuzzy finding or to create a new object.
        zone, created = zone_lookup.prompt(fuzzy_string, defaults={'name': fuzzy_string, cutoff=0.5, n=5) 
