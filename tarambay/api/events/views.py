import datetime
import pytz
from django.db.models import Q
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response

from .serializers import (CategorySerializer, CreateEventSerializer,
                          EventSerializer, InviteEventSerializer,
                          JoinEventSerializer, ReadOnlyEventSerializer)
from api.permissions import EventPermission, IsObjectAdmin
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
            return queryset.filter(Q(private=False) | Q(invited__user=user) | Q(admin=user) | Q(going__user=user)
                ).distinct().order_by('-end', '-start')
        else:
            return queryset.filter(private=False).distinct().order_by('-end', '-start')


class EventInviteView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = InviteEventSerializer
    lookup_field = 'uuid'
    permission_classes = (IsObjectAdmin,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EventSerializer(instance, context={'request':request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = ReadOnlyEventSerializer(instance, context={'request': request})
        return Response(serializer.data)


class EventJoinView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    lookup_field = 'uuid'
    serializer_class = JoinEventSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EventSerializer(instance, context={'request':request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = ReadOnlyEventSerializer(instance, context={'request': request})
        return Response(serializer.data)
