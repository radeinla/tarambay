from django.conf.urls import include, url
from rest_framework import routers

from api.events.views import CategoryViewSet, EventViewSet
from api.users.views import UserViewSet


router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('events', EventViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
