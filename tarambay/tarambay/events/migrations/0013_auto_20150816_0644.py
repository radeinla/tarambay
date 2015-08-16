# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20150816_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.TextField(verbose_name='Location'),
        ),
    ]
