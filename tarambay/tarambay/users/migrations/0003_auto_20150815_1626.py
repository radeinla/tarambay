# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_invited'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invited',
            options={'verbose_name': 'Invited', 'verbose_name_plural': 'Invited'},
        ),
    ]
