from rest_framework import generics, status
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response

from accounts.models import UserProfile
from donations.models import DonorProfile, BloodDonationLog, DonationCenter, DonationSchedule
from donations.serializers import DonationCenterSerializer, DonorProfileSerializer, BloodDonationLogSerializer, \
    DonationScheduleSerializer

from donations.utilities.calendar import create_service


# Create your views here.
# class views for the DonationCenter Model, handles get and post requests
class DonationCenterView(ListCreateAPIView):
    serializer_class = DonationCenterSerializer
    queryset = DonationCenter.objects.all()


# class view for getting, updating and deleting a single donationcenter instance
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
        try:
            if serializer.is_valid():
                # create blood donation schedule

                # create blood donation log
                donor_profile = DonorProfile.objects.filter(user_profile=serializer.validated_data['donor'])[0]
                blood_type = donor_profile.blood_type
                blood_donation_log = BloodDonationLog.objects.create(
                    donor=serializer.validated_data['donor'],
                    donation_center=serializer.validated_data['donation_center'],
                    is_scheduled_donation=True,
                    blood_type=blood_type,
                    additional_notes=serializer.validated_data['additional_notes'],

                    # TODO: create a signal to assign a volunteer if not created and assigned
                    # assigned_volunteer=serializer.validated_data['assigned_volunteer'],

                )

                instance = serializer.save(blood_donation_log=blood_donation_log)

                # add the schedule donation to the user's google calendar 
                user = donor_profile.user
                service = create_service(user)

                # event to add to the user's calendar 

                event = {
                    'summary': 'Donation Schedule',
                    'location': 'Donation Center',
                    'description': 'Donation details',
                    'start': {
                        'dateTime': '2023-12-01T09:00:00',
                        'timeZone': 'America/Los_Angeles',
                    },
                    'end': {
                        'dateTime': '2023-12-01T17:00:00',
                        'timeZone': 'America/Los_Angeles',
                    },
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'email', 'minutes': 24 * 60},
                            {'method': 'popup', 'minutes': 10},
                        ],
                    },
                }

                # method creates the event in the user's calendar 
                event = service.events().insert(calendarId='primary', body=event).execute()

                # returns a response
                return Response(
                    {
                        "message": "Blood donation schedule created successfully",
                        "instance": instance,
                    },
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DonationScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DonationScheduleSerializer
    queryset = DonationSchedule.objects.all()
    lookup_field = 'id'
