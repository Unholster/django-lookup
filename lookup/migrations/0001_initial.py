# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('domain', models.CharField(max_length=255, db_index=True)),
                ('key', models.TextField(max_length=255)),
                ('target_id', models.PositiveIntegerField()),
                ('target_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='alias',
            unique_together=set([('domain', 'key')]),
        ),
    ]
