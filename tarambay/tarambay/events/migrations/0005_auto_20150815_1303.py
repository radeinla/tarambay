# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='admin',
            field=models.OneToOneField(related_name='admin', to=settings.AUTH_USER_MODEL),
        ),
    ]
