import random

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Role, User, UserActivation, UserProfile
from accounts.serializers import RoleSerializer, UserSerializer, UserActivationSerializer, LoginSerializer, \
    UserProfileSerializer
from accounts.utilities.activation import send_email, generate_activation


# Create your views here.


class CreateRoleView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class GetAllRolesView(ListAPIView):
    """Get all roles view"""

    serializer_class = RoleSerializer
    queryset = Role.objects.all()


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.validated_data['is_active'] = False
            serializer.validated_data['is_staff'] = False
            activation_key = generate_activation()
            print(activation_key)
            print(serializer.validated_data)
            serializer.save()
            activate = UserActivation.objects.create(user_id=serializer.data['id'], activation_key=activation_key)
            activate.save()
            send_email(serializer.data['email'], activation_key)
            # send_sms(serializer.data['username'], activation_key)
            serializer.validated_data['password'] = ''
            print(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendActivationCodeView(generics.CreateAPIView):
    serializer_class = UserActivationSerializer
    queryset = UserActivation.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserActivationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            try:
                user = User.objects.get(id=user.id)
            except User.DoesNotExist:
                return Response("User not found", status=status.HTTP_404_NOT_FOUND)

            activation_key = generate_activation()
            activate, _created = UserActivation.objects.update_or_create(
                user_id=user.id,
                defaults={'activation_key': activation_key}
            )

            try:
                activate.save()
            except Exception as e:
                return Response(f"Error saving activation: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            result = send_email(user.email, activation_key)

            if result:
                return Response('Activation code sent', status=status.HTTP_200_OK)
            else:
                return Response('Error sending activation code', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(generics.RetrieveAPIView):
    serializer_class = UserActivationSerializer
    queryset = UserActivation.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):

        serializer = UserActivationSerializer(data=request.data)
        if serializer.is_valid():
            real_code = UserActivation.objects.filter(user_id=serializer.validated_data['user'],
                                                      activation_key=serializer.validated_data['activation_key'])
            if real_code:
                user = User.objects.get(id=request.data['user'])
                user.is_active = True
                user.save()
                return Response('Activation successful', status=status.HTTP_200_OK)
            return Response('Activation Failed, check your code', status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]

    def post(self, request, format=None, **kwargs):
        print(2)
        print(request.data)
        user = UserSerializer(authenticate(username=request.data['username'], password=request.data['password']))
        if user.data.get('id'):
            print(user.data)
            user1 = User(user.data['id'])
            print(user1)
            if user:
                refresh = RefreshToken.for_user(user1)
                print(refresh)
                res = {
                    'user': user.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(res, status=status.HTTP_200_OK)
        return Response('wrong username or password', status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'user'


class GetAllUserProfilesView(ListAPIView):
    """Get all User Profiles view"""

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


