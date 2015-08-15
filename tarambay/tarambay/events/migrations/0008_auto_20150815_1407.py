# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20150815_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='going',
            field=models.ManyToManyField(related_name='going_events', null=True, to='users.Invited', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='invited',
            field=models.ManyToManyField(related_name='invited_events', null=True, to='users.Invited', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='latitude',
            field=models.DecimalField(verbose_name='Latitude', max_digits=9, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='event',
            name='longitude',
            field=models.DecimalField(verbose_name='Longitude', max_digits=9, decimal_places=6),
        ),
    ]
