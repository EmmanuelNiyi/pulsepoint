from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import ListAPIView

from donations.models import DonorProfile
from donations.serializers import DonorProfileSerializer


# Create your views here.



class DonorProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DonorProfileSerializer
    queryset = DonorProfile.objects.all()
    lookup_field = 'user'


class GetAllDonorProfilesView(ListAPIView):
    """Get all Donor Profiles view"""

    serializer_class = DonorProfileSerializer
    queryset = DonorProfile.objects.all()