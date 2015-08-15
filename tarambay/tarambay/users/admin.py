from django.contrib import admin

from .models import User, Invited


admin.site.register(User)
admin.site.register(Invited)
