from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from pygeocoder import Geocoder
from rest_framework import serializers
from rest_framework.reverse import reverse

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
    going = InvitedSerializer(many=True)
    invite_url = serializers.SerializerMethodField()
    join_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'self', 'category', 'title', 'description', 'latitude',
                  'longitude', 'start', 'end', 'admin', 'tags', 'invited',
                  'going', 'invite_url', 'join_url', 'private', 'location')
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'},
            'admin': {'lookup_field': 'uuid'},
            'category': {'lookup_field': 'uuid'},
        }

    def get_invite_url(self, obj):
        return reverse('event-invite', args=[obj.uuid], request=self.context['request'])

    def get_join_url(self, obj):
        return reverse('event-join', args=[obj.uuid], request=self.context['request'])


class CreateEventSerializer(EventSerializer):
    location = serializers.CharField(required=False, allow_blank=True)
    latitude = serializers.CharField(required=False, allow_blank=True)
    longitude = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Event
        fields = ('id', 'self', 'category', 'title', 'description', 'location',
                  'latitude', 'longitude', 'start', 'end', 'tags', 'private')
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
                data['location'] = result.formatted_address
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


class JoinEventSerializer(serializers.Serializer):
    join = serializers.BooleanField(write_only=True)

    def update(self, instance, validated_data):
        join = validated_data.get('join')
        user = self.context['request'].user
        try:
            instance.going.get(user=user)
            return instance
        except Invited.DoesNotExist:
            pass
        if join:
            if instance.admin:
                try:
                    invited = instance.invited.get(user=user)
                except Invited.DoesNotExist:
                    invited, created = Invited.objects.get_or_create(user=user)
                instance.invited.remove(invited)
                instance.going.add(invited)
            elif instance.private:
                try:
                    invited = instance.invited.get(user=user)
                    instance.invited.remove(invited)
                except Invited.DoesNotExist:
                    raise serializers.ValidationError(_("You can only join "
                        "private events you have been invited to."))
                instance.going.add(invited)
            else:
                try:
                    invited = instance.invited.get(user=user)
                    instance.invited.remove(invited)
                except Invited.DoesNotExist:
                    invited, created = Invited.objects.get_or_create(user=user)
                instance.going.add(invited)
        return instance


class ReadOnlyEventSerializer(EventSerializer):
    class Meta:
        model = Event
        fields = ('id', 'self', 'category', 'title', 'description', 'latitude',
                  'longitude', 'start', 'end', 'admin', 'tags', 'invited',
                  'going', 'invite_url', 'join_url', 'private', 'location')
        read_only_fields = ('id', 'self', 'category', 'title', 'description', 'latitude',
                  'longitude', 'start', 'end', 'admin', 'tags', 'invited',
                  'going', 'invite_url', 'join_url', 'private', 'location')
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'},
            'admin': {'lookup_field': 'uuid'},
            'category': {'lookup_field': 'uuid'},
        }