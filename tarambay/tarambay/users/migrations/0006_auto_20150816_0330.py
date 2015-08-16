# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150816_0329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invited',
            name='uuid',
            field=django_extensions.db.fields.UUIDField(unique=True, editable=False, blank=True),
        ),
    ]
