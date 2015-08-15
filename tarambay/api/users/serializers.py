from rest_framework import serializers

from tarambay.users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'self', 'username',)
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'}
        }


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'self', 'username', 'first_name', 'last_name', 'email',
                  'is_staff')
        read_only_fields = ('is_staff',)
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'}
        }
