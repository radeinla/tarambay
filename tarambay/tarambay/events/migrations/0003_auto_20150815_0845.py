# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150815_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='uuid',
            field=django_extensions.db.fields.UUIDField(unique=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='uuid',
            field=django_extensions.db.fields.UUIDField(unique=True, editable=False, blank=True),
        ),
    ]
