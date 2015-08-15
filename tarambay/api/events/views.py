from rest_framework import viewsets

from .serializers import CategorySerializer
from tarambay.events.models import Category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'uuid'
