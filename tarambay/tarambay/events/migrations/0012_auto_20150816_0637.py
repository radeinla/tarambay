# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from pygeocoder import Geocoder


def add_location(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    for event in Event.objects.all():
        result = Geocoder.reverse_geocode(event.latitude, event.longitude)
        event.location = result.formatted_address
        event.save()

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_event_location'),
    ]

    operations = [
        migrations.RunPython(add_location),
    ]
