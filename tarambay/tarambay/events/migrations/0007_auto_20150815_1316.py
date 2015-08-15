# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150815_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='admin',
            field=models.ForeignKey(related_name='events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ForeignKey(related_name='events', verbose_name='Category', to='events.Category'),
        ),
        migrations.AlterField(
            model_name='event',
            name='going',
            field=models.ManyToManyField(related_name='going_events', to='users.Person'),
        ),
        migrations.AlterField(
            model_name='event',
            name='invited',
            field=models.ManyToManyField(related_name='invited_events', to='users.Person'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.ForeignKey(related_name='events', verbose_name='Location', to='events.Location'),
        ),
    ]
