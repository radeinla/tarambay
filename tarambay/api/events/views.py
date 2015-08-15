from rest_framework import viewsets

from .serializers import CategorySerializer, EventSerializer
from tarambay.events.models import Category, Event


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'uuid'


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'uuid'
