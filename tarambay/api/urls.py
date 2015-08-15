from django.conf.urls import include, url
from rest_framework import routers

from api.events.views import CategoryViewSet
from api.users.views import UserViewSet


router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
