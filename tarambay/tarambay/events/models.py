from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=255, db_index=True)
    description = models.TextField(_('Description'), blank=True)
    slug = models.SlugField(_('Slug'), max_length=255, db_index=True,
                            editable=False)


class Location(models.Model):
    latitude = models.DecimalField(_('Latitude'), decimal_places=6,
                                   max_digits=9, blank=True, null=True)
    longitude = models.DecimalField(_('Longitude'), decimal_places=6,
                                    max_digits=9, blank=True, null=True)


class Event(models.Model):
    category = models.OneToOneField('events.Category', related_name='category',
                                    verbose_name=_('Category'))
    location = models.OneToOneField('events.Location', related_name='location',
                                    verbose_name=_('Location'))
    title = models.CharField(_('Title'), max_length=255, db_index=True)
    description = models.TextField(_('Description'), blank=True)
    start = models.DateTimeField(_('Start'))
    end = models.DateTimeField(_('End'))
    tags = TagField()