from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import DonationCenter, Volunteer


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