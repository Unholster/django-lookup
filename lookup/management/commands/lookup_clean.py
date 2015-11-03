# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from lookup.legacy import LookupTable
from optparse import make_option

class Command(BaseCommand):
    args='app.model'
    help = 'Elimina aliases huérfanos para un modelo'
    option_list = BaseCommand.option_list + (
            make_option('--all',
                    action='store_true',
                    dest='all',
                    default=False,
                    help='Elimina los aliases huerfanos para todos los modelos'
                ),
        )

    def handle(self, *fq_model_names, **options):
        if options['all']:
            types = ContentType.objects.all()
        else:
            types = self.types_for_modelnames(fq_model_names)

        for t in types:
            table = LookupTable(t.model_class())
            table.clean()

    def types_for_modelnames(self, fq_model_names):
        for fq_name in fq_model_names:
            app_label, model_name = fq_name.rsplit(".", 1)
            yield ContentType.objects.get(
                    app_label=app_label,
                    model=model_name
                )
