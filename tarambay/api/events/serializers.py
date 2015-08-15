from rest_framework import serializers

from tarambay.events.models import Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'self', 'name', 'description')
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'}
        }
