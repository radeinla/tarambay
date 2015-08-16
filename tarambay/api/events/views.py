import datetime
import pytz
from django.db.models import Q
from rest_framework import permissions, viewsets

from .serializers import CategorySerializer, CreateEventSerializer, EventSerializer
from api.permissions import EventPermission
from tarambay.events.models import Category, Event


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'uuid'
    permission_classes = (permissions.AllowAny,)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.none()
    serializer_class = EventSerializer
    create_serializer_class = CreateEventSerializer
    lookup_field = 'uuid'
    permission_classes = (EventPermission,)

    def get_serializer_class(self):
        ACTIONS = ['create', 'update', 'partial_update']
        if self.action in ACTIONS:
            return self.create_serializer_class
        else:
            return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        now = datetime.datetime.now(pytz.utc)
        queryset = Event.objects.filter(start__gt=now)
        if user.is_authenticated():
            return queryset.filter(Q(private=False) | Q(invited__user=user)).order_by('-end', '-start')
        else:
            return queryset.filter(private=False).order_by('-end', '-start')
