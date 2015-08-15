# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0003_auto_20150815_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='admin',
            field=models.OneToOneField(related_name='admin', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
