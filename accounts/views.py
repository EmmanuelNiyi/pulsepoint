from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListAPIView

from accounts.models import Role
from accounts.serializers import RoleSerializer


# Create your views here.


class CreateRoleView(generics.CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class GetAllRolesView(ListAPIView):
    """Get all roles view"""

    serializer_class = RoleSerializer
    queryset = Role.objects.all()
