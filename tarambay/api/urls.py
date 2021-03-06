from django.conf.urls import include, url
from rest_framework import routers

from api.events.views import (CategoryViewSet, EventViewSet, EventInviteView,
                              EventJoinView)
from api.users.views import ProfileView, RegisterView, UserViewSet


router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('events', EventViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    url(r'^events/(?P<uuid>[^/.]+)/invited/$', EventInviteView.as_view(), name='event-invite'),
    url(r'^events/(?P<uuid>[^/.]+)/join/$', EventJoinView.as_view(), name='event-join'),
    url(r'^users/profile', ProfileView.as_view(), name='user-profile'),
    url(r'^users/register', RegisterView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
