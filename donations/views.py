from rest_framework import generics, status
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response

from accounts.models import UserProfile
from donations.models import DonorProfile, BloodDonationLog, DonationCenter, DonationSchedule
from donations.serializers import DonationCenterSerializer, DonorProfileSerializer, BloodDonationLogSerializer, \
    DonationScheduleSerializer



# Create your views here.
# class views for the DonationCenter Model, handles get and post requests
class DonationCenterView(ListCreateAPIView):
    serializer_class = DonationCenterSerializer
    queryset = DonationCenter.objects.all()


# class view for getting, updating and deleting a single donation center instance
class DonationCenterDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DonationCenterSerializer
    queryset = DonationCenter.objects.all()
    lookup_field = 'id'


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

    serializer_class = BloodDonationLogSerializer
    queryset = BloodDonationLog.objects.all()

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
    serializer_class = BloodDonationLogSerializer
    queryset = BloodDonationLog.objects.all()
    lookup_field = 'id'

    # LookUp field does the job of the code below
    # def get_queryset(self):
    #     business = self.request.user
    #     print(self.kwargs["pk"])
    #     return BloodDonation.objects.filter(id=self.kwargs['pk'])


class GetAllUserBloodDonationView(generics.ListAPIView):
    """Get all of a businesses expenses"""

    serializer_class = BloodDonationLogSerializer
    queryset = BloodDonationLog.objects.all()

    def get_queryset(self):
        user = self.request.user
        user_profile = UserProfile.objects.filter(user_id=user.id)[0]
        return BloodDonationLog.objects.filter(donor=user_profile)


class DonationScheduleCreationView(CreateAPIView):
    """
    Create a new blood donation schedule for a donor
    """

    serializer_class = DonationScheduleSerializer
    queryset = DonationSchedule.objects.all()

    def perform_create(self, serializer):
        """
        Method to perform the creation of a blood donation schedule and log for a donor.
        Takes a serializer as input. Returns a response with a success or error message.
        """
        try:
            if serializer.is_valid():
                # Retrieve the donor profile based on the validated data
                donor_profile = DonorProfile.objects.get(user_profile=serializer.validated_data['donor'])

                # Get the blood type from the donor profile
                blood_type = donor_profile.blood_type

                # Create a new blood donation log with the donor, donation center, blood type, and additional notes
                blood_donation_log = BloodDonationLog.objects.create(
                    donor=serializer.validated_data['donor'],
                    donation_center=serializer.validated_data['donation_center'],
                    is_scheduled_donation=True,
                    blood_type=blood_type,
                    additional_notes=serializer.validated_data['additional_notes'],
                )

                # Save the blood donation log in the serializer instance
                instance = serializer.save(blood_donation_log=blood_donation_log)


                # Return a response with a success message and the created instance
                return Response(
                    {
                        "message": "Blood donation schedule created successfully",
                        "instance": instance
                    },
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DonationScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DonationScheduleSerializer
    queryset = DonationSchedule.objects.all()
    lookup_field = 'id'