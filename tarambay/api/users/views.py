from rest_framework import viewsets

from .serializers import UserSerializer
from tarambay.users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'
