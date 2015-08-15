# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('slug', models.SlugField(verbose_name='Slug', max_length=255, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title', db_index=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('start', models.DateTimeField(verbose_name='Start')),
                ('end', models.DateTimeField(verbose_name='End')),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('category', models.OneToOneField(related_name='category', verbose_name='Category', to='events.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.DecimalField(null=True, verbose_name='Latitude', max_digits=9, decimal_places=6, blank=True)),
                ('longitude', models.DecimalField(null=True, verbose_name='Longitude', max_digits=9, decimal_places=6, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.OneToOneField(related_name='location', verbose_name='Location', to='events.Location'),
        ),
    ]
