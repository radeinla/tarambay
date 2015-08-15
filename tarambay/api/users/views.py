from rest_framework import generics, permissions, viewsets

from .serializers import ProfileSerializer, RegisterSerializer, UserSerializer
from api.permissions import IsAnonUser, IsObjectUser
from tarambay.users.models import User


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'
    permission_classes = (permissions.AllowAny,)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.none()
    serializer_class = ProfileSerializer
    lookup_field = 'uuid'
    permission_class = (IsObjectUser,)

    def get_object(self):
        return self.request.user


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (IsAnonUser,)
