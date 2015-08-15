# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20150815_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='going',
            field=models.ManyToManyField(related_name='going_events', to='users.Invited', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='invited',
            field=models.ManyToManyField(related_name='invited_events', to='users.Invited', blank=True),
        ),
    ]
