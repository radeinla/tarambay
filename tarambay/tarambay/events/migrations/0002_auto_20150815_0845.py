# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='uuid',
            field=django_extensions.db.fields.UUIDField(unique=True, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='uuid',
            field=django_extensions.db.fields.UUIDField(unique=True, null=True, editable=False, blank=True),
        ),
    ]
