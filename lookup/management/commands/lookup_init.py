# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from lookup.legacy import LookupTable

class Command(BaseCommand):
    args='app.model.field'
    help = 'Inicializa la tabla de lookup de un modelo en base a un campo del modelo'

    def handle(self, *fq_model_names, **kwargs):
        for fq_name in fq_model_names:
            field_name = None
            app_label, model_name = fq_name.split(".", 1)

            try:
                model_name, field_name = model_name.split(".", 1)
            except:
                pass

            content_type = ContentType.objects.get(
                    app_label=app_label,
                    model=model_name
                )
            table = LookupTable(content_type.model_class())
            table.create_aliases(field_name)
