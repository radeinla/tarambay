# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models, migrations


def add_uuid(apps, schema_editor):
    Invited = apps.get_model('users', 'Invited')
    for invited in Invited.objects.all():
        invited.uuid = u'' + str(uuid.uuid1().hex)
        invited.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_invited_uuid'),
    ]

    operations = [
        migrations.RunPython(add_uuid),
    ]
