from rest_framework.serializers import ModelSerializer

from accounts.models import UserProfile
from donations.models import InvestigationType, LaboratoryInvestigation, BloodDonation, DonationSchedule, DonorProfile


class InvestigationTypeSerializer(ModelSerializer):
    class Meta:
        model = InvestigationType
        fields = '__all__'


class LaboratoryInvestigationSerializer(ModelSerializer):
    class Meta:
        model = LaboratoryInvestigation
        fields = '__all__'


class BloodDonationSerializer(ModelSerializer):
    class Meta:
        model = BloodDonation
        fields = '__all__'


class DonationScheduleSerializer(ModelSerializer):
    class Meta:
        model = DonationSchedule
        fields = '__all__'


class DonorProfileSerializer(ModelSerializer):
    class Meta:
        model = DonorProfile
        fields = '__all__'