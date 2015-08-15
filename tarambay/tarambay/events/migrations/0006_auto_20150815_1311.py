# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_person'),
        ('events', '0005_auto_20150815_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='going',
            field=models.ManyToManyField(related_name='going', to='users.Person'),
        ),
        migrations.AddField(
            model_name='event',
            name='invited',
            field=models.ManyToManyField(related_name='invited', to='users.Person'),
        ),
    ]
