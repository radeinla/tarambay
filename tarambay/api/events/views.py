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
    queryset = Event.objects.all()
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
