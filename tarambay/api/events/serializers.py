from rest_framework import serializers

from tarambay.events.models import Category, Event, Location


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='uuid')

    class Meta:
        model = Category
        fields = ('id', 'self', 'name', 'description')
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'}
        }


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('latitude', 'longitude')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    location = LocationSerializer()
    id = serializers.UUIDField(source='uuid')

    class Meta:
        model = Event
        fields = ('id', 'self', 'category', 'title', 'description', 'location',
                  'start', 'end', 'admin')
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'},
            'admin': {'lookup_field': 'uuid'},
            'category': {'lookup_field': 'uuid'},
        }


class CreateEventSerializer(EventSerializer):
    location = serializers.CharField(write_only=True)
