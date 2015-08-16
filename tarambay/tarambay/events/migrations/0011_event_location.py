# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_event_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.TextField(null=True, verbose_name='Location', blank=True),
        ),
    ]
