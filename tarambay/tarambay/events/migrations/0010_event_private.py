# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20150815_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
