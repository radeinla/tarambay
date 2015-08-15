from rest_framework import serializers

from tarambay.users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'self', 'username', 'email', 'is_staff')
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'}
        }