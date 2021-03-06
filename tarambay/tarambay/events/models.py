from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import UUIDField
from tagging.fields import TagField


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=255, db_index=True)
    description = models.TextField(_('Description'), blank=True)
    slug = models.SlugField(_('Slug'), max_length=255, db_index=True,
                            editable=False)
    uuid = UUIDField(unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Event(models.Model):
    admin = models.ForeignKey('users.User', related_name='events')
    category = models.ForeignKey('events.Category', related_name='events',
                                    verbose_name=_('Category'))
    title = models.CharField(_('Title'), max_length=255, db_index=True)
    description = models.TextField(_('Description'), blank=True)
    start = models.DateTimeField(_('Start'))
    end = models.DateTimeField(_('End'))
    location = models.TextField(_('Location'))
    latitude = models.DecimalField(_('Latitude'), decimal_places=6,
                                   max_digits=9)
    longitude = models.DecimalField(_('Longitude'), decimal_places=6,
                                    max_digits=9)
    tags = TagField()
    uuid = UUIDField(unique=True)
    invited = models.ManyToManyField('users.Invited', related_name='invited_events',
                                     blank=True)
    going = models.ManyToManyField('users.Invited', related_name='going_events',
                                   blank=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        return "{} start: {} end: {}".format(self.title, self.start, self.end)
