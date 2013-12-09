from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

class Alias(models.Model):
    key = models.TextField(max_length=255)
    target_type = models.ForeignKey(ContentType)
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_type', 'target_id')

    class Meta:
        unique_together = ('key', 'target_type')

class Dummy(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name