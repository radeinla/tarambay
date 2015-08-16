from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from pygeocoder import Geocoder
from rest_framework import serializers

from api.users.serializers import InvitedSerializer
from tarambay.events.models import Category, Event
from tarambay.users.models import Invited, User


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='uuid')

    class Meta:
        model = Category
        fields = ('id', 'self', 'name', 'description')
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'}
        }


class EventSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)
    invited = InvitedSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'self', 'category', 'title', 'description', 'latitude',
                  'longitude', 'start', 'end', 'admin', 'tags', 'invited')
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'},
            'admin': {'lookup_field': 'uuid'},
            'category': {'lookup_field': 'uuid'},
        }


class CreateEventSerializer(EventSerializer):
    location = serializers.CharField(write_only=True, required=False, allow_blank=True)
    latitude = serializers.CharField(required=False, allow_blank=True)
    longitude = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Event
        fields = ('id', 'self', 'category', 'title', 'description', 'location',
                  'latitude', 'longitude', 'start', 'end', 'tags')
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'},
            'admin': {'lookup_field': 'uuid'},
            'category': {'lookup_field': 'uuid'},
        }

    def validate(self, data):
        """
        Check that location is a valid address
        """
        location = data.pop('location', None)
        start = data.get('start', None)
        end = data.get('end', None)
        if location:
            result = Geocoder.geocode(location)
            if result.valid_address:
                data['latitude'] = result.latitude
                data['longitude'] = result.longitude
            else:
                raise serializers.ValidationError(_("That is not a valid location."))
        if start and end:
            if end <= start:
                raise serializers.ValidationError("The end date and time must be \
                    after the start date and time")
        elif not self.partial:
            latitude = data.get('latitude', None)
            longitude = data.get('longitude', None)
            if not latitude or not longitude:
                raise serializers.ValidationError(_(
                    "Either a valid address for location should be provided or"
                    " latitude and longitude should be provided."))
        if self.partial:
            return data
        data['admin'] = self.context['request'].user
        return data

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class InviteEventSerializer(serializers.ModelSerializer):
    invited = serializers.CharField(write_only=True)

    class Meta:
        model = Event
        fields = ('invited',)

    def update(self, instance, validated_data):
        # invited is a comma-separated string of either usernames or emails
        # disregards input that is not a valid username or email
        invited_list = validated_data['invited'].split(", ")
        for item in invited_list:
            user = None
            email = None
            try:
                user = User.objects.get(username=item)
            except User.DoesNotExist:
                try:
                    validate_email(item)
                    email = item
                except ValidationError:
                    continue
            if email:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    invited, created = Invited.objects.get_or_create(email=email)
            if user:
                invited, created = Invited.objects.get_or_create(user=user)
            instance.invited.add(invited)
        return instance
