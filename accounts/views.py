import random

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Role, User, UserActivation
from accounts.serializers import RoleSerializer, UserSerializer, UserActivationSerializer, LoginSerializer
from accounts.utilities.activation import send_email


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
            print(serializer.validated_data)
            user = serializer.validated_data['user']
            user = User.objects.get(id=user.id)
            activation_key = generate_activation()

            # activate = UserActivation.objects.create(user_id=serializer.validated_data['user'],
            #                                          activation_key=activation_key)

            activate, _created = UserActivation.objects.update_or_create(user_id=user.id,
                                                                         defaults={'activation_key': activation_key})

            activate.save()
            result = send_email(user.email, activation_key)

            if result == 1:
                return Response(f'Activation code sent', status=status.HTTP_200_OK)
            else:
                return Response(f'Activation code not sent', status=status.HTTP_400_BAD_REQUEST)
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


# class UserProfileView(generics.CreateAPIView):
#     serializer_class = ProfileSerializer
#     queryset = Profile.objects.all()
#
#
# class UserProfileDetailView(generics.RetrieveUpdateAPIView):
#     serializer_class = ProfileSerializer
#     queryset = Profile.objects.all()
#     lookup_field = 'user'


def generate_activation():
    res = ""
    for _ in range(1, 6):
        x = random.randint(1, 10)
        res = res + str(x)
    return res