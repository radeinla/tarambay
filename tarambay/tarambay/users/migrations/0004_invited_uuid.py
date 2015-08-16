# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150815_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='invited',
            name='uuid',
            field=django_extensions.db.fields.UUIDField(unique=True, null=True, editable=False, blank=True),
        ),
    ]
