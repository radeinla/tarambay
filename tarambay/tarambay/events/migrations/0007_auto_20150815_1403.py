# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150815_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='location',
        ),
        migrations.AddField(
            model_name='event',
            name='latitude',
            field=models.DecimalField(null=True, verbose_name='Latitude', max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='longitude',
            field=models.DecimalField(null=True, verbose_name='Longitude', max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
