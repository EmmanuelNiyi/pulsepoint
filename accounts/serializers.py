from datetime import datetime

from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import Role, UserActivation, User, UserProfile


# User = settings.AUTH_USER_MODEL


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'roles']
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        # extra_kwargs = {'password': {'write_only': True}}


class UserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['last_name']


class UserActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivation
        extra_kwargs = {'activation_key': {'write_only': True, 'required': False}}
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'



