from datetime import datetime

from django.conf import settings
from rest_framework.serializers import ModelSerializer

from accounts.models import Role

User = settings.AUTH_USER_MODEL


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

