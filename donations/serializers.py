from datetime import datetime
from .models import DonationCenter, Volunteer, InvestigationType, LaboratoryInvestigation, BloodDonationLog, DonationSchedule, DonorProfile
from rest_framework.serializers import ModelSerializer



# this is the serializer for all the fields of Donation Center
class DonationCenterSerializer(ModelSerializer):
    class Meta:
        model = DonationCenter
        fields = '__all__'


# Serializer for just accreditation status and date of Donation center
class AccreditationSerializer(ModelSerializer):
    class Meta:
        model = DonationCenter
        fields = ['accreditation_status', 'accreditation_date']


# Serializer for all the fields of Volunteer Object
class VolunteerSerializer(ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'


class InvestigationTypeSerializer(ModelSerializer):
    class Meta:
        model = InvestigationType
        fields = '__all__'


class LaboratoryInvestigationSerializer(ModelSerializer):
    class Meta:
        model = LaboratoryInvestigation
        fields = '__all__'


class BloodDonationLogSerializer(ModelSerializer):
    class Meta:
        model = BloodDonationLog
        fields = '__all__'


class DonationScheduleSerializer(ModelSerializer):
    class Meta:
        model = DonationSchedule
        fields = '__all__'


class DonorProfileSerializer(ModelSerializer):
    class Meta:
        model = DonorProfile
        fields = '__all__'
