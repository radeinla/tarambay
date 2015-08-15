from django.contrib import admin

from .models import Category, Location, Event


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Event)
