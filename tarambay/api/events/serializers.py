from rest_framework import serializers

from tarambay.events.models import Category, Event


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='uuid')

    class Meta:
        model = Category
        fields = ('id', 'self', 'name', 'description')
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'}
        }


class EventSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    id = serializers.UUIDField(source='uuid')

    class Meta:
        model = Event
        fields = ('id', 'self', 'category', 'title', 'description', 'location',
                  'start', 'end')
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'}
        }

    def get_category(self, obj):
        return obj.category.name

    def get_location(self, obj):
        return "{}, {}".format(obj.location.latitude, obj.location.longitude)
