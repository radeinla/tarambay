from rest_framework import permissions, viewsets

from .serializers import CategorySerializer, EventSerializer
from tarambay.events.models import Category, Event


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'uuid'
    permission_classes = (permissions.AllowAny,)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'uuid'
