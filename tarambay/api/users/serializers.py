from rest_framework import serializers
from rest_framework.reverse import reverse

from tarambay.core.utils import normalise_email
from tarambay.users.models import Invited, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'self', 'username',)
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'}
        }


class RegisterSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)
    profile = serializers.SerializerMethodField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'self', 'profile', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'username')
        extra_kwargs = {
            'self': {'lookup_field': 'uuid'}
        }

    def get_profile(self, obj):
        return reverse('user-profile', request=self.context['request'])

    def check_if_user_exists(self, email):
        email = normalise_email(email)
        if User._default_manager.filter(email__iexact=email).exists():
            raise serializers.ValidationError(_("A user with that email "
                                                "address already exists"))

    def check_password_identical(self, password1, password2):
        if password1 != password2:
            raise serializers.ValidationError(_("The two password fields "
                                                "didn't match."))

    def create(self, validated_data):
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)
        username = validated_data.get('username', None)
        self.check_if_user_exists(validated_data['email'])
        user = User(
            email=validated_data['email']
        )
        self.check_password_identical(validated_data['password1'],
                                      validated_data['password2'])
        user.set_password(validated_data['password1'])
        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        # created invited object on user creation
        Invited.objects.create(user=user)
        return user


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


class InvitedSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.SerializerMethodField()

    class Meta:
        model = Invited
        fields = ('username', 'email')

    def get_email(self, obj):
        if obj.user:
            return obj.user.email
        else:
            return obj.email