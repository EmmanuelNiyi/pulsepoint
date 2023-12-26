from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from accounts.models import UserProfile
from donations.models import DonorProfile, BloodDonation
from donations.serializers import DonorProfileSerializer, BloodDonationSerializer


# Create your views here.


class DonorProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DonorProfileSerializer
    queryset = DonorProfile.objects.all()
    lookup_field = 'user'


class GetAllDonorProfilesView(ListAPIView):
    """Get all Donor Profiles view"""

    serializer_class = DonorProfileSerializer
    queryset = DonorProfile.objects.all()


class CreateBloodDonationView(CreateAPIView):
    """
    Register a new blood donation


    Try it out
    """

    serializer_class = BloodDonationSerializer
    queryset = BloodDonation.objects.all()

    def perform_create(self, serializer):
        try:
            if serializer.is_valid():
                instance = serializer.save()
                print(instance)
                return Response(
                    {
                        "message": "Blood donation registered successfully",
                        "instance": instance,
                    },
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BloodDonationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BloodDonationSerializer
    queryset = BloodDonation.objects.all()
    lookup_field = 'id'

    # LookUp field does the job of the code below
    # def get_queryset(self):
    #     business = self.request.user
    #     print(self.kwargs["pk"])
    #     return BloodDonation.objects.filter(id=self.kwargs['pk'])


class GetAllUserBloodDonationView(generics.ListAPIView):
    """Get all of a businesses expenses"""

    serializer_class = BloodDonationSerializer
    queryset = BloodDonation.objects.all()

    def get_queryset(self):
        user = self.request.user
        user_profile = UserProfile.objects.filter(user_id=user.id)[0]
        return BloodDonation.objects.filter(donor=user_profile)
