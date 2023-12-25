from django.db import models
from accounts.models import User, TimeStampedModel


class DonationCenter(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    location_address = models.CharField(max_length=255)
    location_city = models.CharField(max_length=100)
    location_state = models.CharField(max_length=50)
    location_zipcode = models.CharField(max_length=20, null=True, blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)

    ACCREDITATION_STATUS_CHOICES = [
        ('Accredited', 'Accredited'),
        ('Pending', 'Pending Accreditation'),
        ('Not Accredited', 'Not Accredited')
    ]
    accreditation_status = models.CharField(max_length=50, choices=ACCREDITATION_STATUS_CHOICES, default='Not Accredited')
    accreditation_date = models.DateField(null=True, blank=True)

    opening_time = models.TimeField()
    closing_time = models.TimeField()

    appointment_availability = models.BooleanField(default=False)
    appointment_scheduling_system = models.CharField(max_length=100, null=True, blank=True) #If Available

    notification_preferences = models.CharField(max_length=100, blank=True)
    additional_notes = models.TextField(blank=True)

    def __str__(self):
        return f"DonationCenter - {self.name}"


class Volunteer(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    availability_days_times = models.TextField()
    preferred_roles = models.CharField(max_length=100, blank=True)
    affiliated_donation_centers = models.ManyToManyField(DonationCenter, related_name='volunteers')

    volunteer_status = models.CharField(max_length=100, blank=True)
    volunteer_hours_logged = models.PositiveIntegerField(default=0)

    CERTIFICATION_STATUS_CHOICES = [
        ('Certified', 'Certified'),
        ('Not Certified', 'Not Certified')
    ]
    certification_status = models.CharField(max_length=50, choices=CERTIFICATION_STATUS_CHOICES, default='Not Certified')
    training_completion_dates = models.DateField(null=True, blank=True)

    communication_preferences = models.CharField(max_length=100, blank=True)
    volunteer_shift_notifications = models.BooleanField(default=True)

    consent_share_information = models.BooleanField(default=False)
    acknowledgment_of_policies = models.BooleanField(default=False)
    additional_notes = models.TextField(blank=True)

    VERIFICATION_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified')
    ]
    verification_status = models.CharField(max_length=50, choices=VERIFICATION_STATUS_CHOICES, default='Pending')
    date_of_verification = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Volunteer - {self.user.username}"