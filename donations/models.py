from django.db import models
from accounts.models import User, TimeStampedModel, UserProfile
from datetime import timedelta, timezone


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
    accreditation_status = models.CharField(max_length=50, choices=ACCREDITATION_STATUS_CHOICES,
                                            default='Not Accredited')
    accreditation_date = models.DateField(null=True, blank=True)

    opening_time = models.TimeField()
    closing_time = models.TimeField()

    appointment_availability = models.BooleanField(default=False)
    appointment_scheduling_system = models.CharField(max_length=100, null=True, blank=True)  # If Available

    notification_preferences = models.CharField(max_length=100, blank=True)
    additional_notes = models.TextField(blank=True)

    def __str__(self):
        return f"DonationCenter - {self.name}"


class Volunteer(TimeStampedModel):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    availability_days_times = models.TextField()
    preferred_roles = models.CharField(max_length=100, blank=True)
    affiliated_donation_centers = models.ManyToManyField(DonationCenter, related_name='volunteers')

    volunteer_status = models.CharField(max_length=100, blank=True)
    volunteer_hours_logged = models.PositiveIntegerField(default=0)

    CERTIFICATION_STATUS_CHOICES = [
        ('Certified', 'Certified'),
        ('Not Certified', 'Not Certified')
    ]
    certification_status = models.CharField(max_length=50, choices=CERTIFICATION_STATUS_CHOICES,
                                            default='Not Certified')
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


class InvestigationType(TimeStampedModel):
    """Not in use"""
    name = models.CharField(max_length=255)
    description = models.TextField()


class LaboratoryInvestigation(TimeStampedModel):
    """Not in use"""
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    investigation = models.ForeignKey(InvestigationType, on_delete=models.DO_NOTHING)
    result = models.TextField(null=True, blank=True)
    date = models.DateField()
    additional_notes = models.TextField(null=True, blank=True)


# Model to handle Blood Donations
class BloodDonationLog(TimeStampedModel):
    donor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    donation_date_time = models.DateTimeField()
    donation_center = models.ForeignKey(DonationCenter, on_delete=models.CASCADE)
    blood_type = models.CharField(
        max_length=5)  # Assuming blood type can be represented as a string (e.g., 'A+', 'B-', etc.)
    donation_quantity = models.PositiveIntegerField()
    health_assessment = models.TextField(null=True, blank=True)
    processing_status = models.CharField(max_length=255, null=True, blank=True)
    storage_information = models.TextField(null=True, blank=True)
    additional_notes = models.TextField(null=True, blank=True)
    is_scheduled_donation = models.BooleanField(default=False)  # to know if it was scheduled on this platform

    assigned_volunteer = models.ForeignKey(Volunteer, on_delete=models.DO_NOTHING, null=True, blank=True)

    # Information about peripheral investigations
    laboratory_investigations = models.ForeignKey(LaboratoryInvestigation, on_delete=models.DO_NOTHING,
                                                  null=True, blank=True)  # NOT IN USE FOR NOW

    def __str__(self):
        return f"BloodDonation - {self.donor.user.username} - {self.donation_date_time}"


class DonationSchedule(TimeStampedModel):
    donor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    volunteer_assignment_status = models.BooleanField(default=False)
    assigned_volunteer = models.ForeignKey(Volunteer, on_delete=models.DO_NOTHING, null=True, blank=True)

    # use a pre_save signal to create this
    blood_donation = models.OneToOneField(BloodDonationLog, on_delete=models.DO_NOTHING)
    scheduled_date_time = models.DateTimeField()
    donation_center = models.ForeignKey(DonationCenter, on_delete=models.CASCADE)

    appointment_status = models.CharField(max_length=50)
    reminder_settings = models.CharField(max_length=50, null=True, blank=True)
    health_assessment = models.TextField(null=True, blank=True)
    notification_preferences = models.CharField(max_length=50, null=True, blank=True)
    additional_notes = models.TextField(blank=True)

    def __str__(self):
        return f"DonationSchedule - {self.donor.user.username} - {self.scheduled_date_time}"





class DonorProfile(models.Model):
    # blood type choices
    BLOOD_TYPE_CHOICES = [('A+', 'A+'), ('A-', 'A-'), 
                            ('B+', 'B+'), ('B-', 'B-'),
                            ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')]

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)  # a user cannot have more than donor profile at a time 
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=5, choices= BLOOD_TYPE_CHOICES, blank=True)   # should this be allowed to be blank
    medical_conditions = models.TextField(blank=True)

    # Donation History
    total_donations = models.PositiveIntegerField(default=0)
    last_donation_date = models.DateField(null=True, blank=True)
    quantity_donated = models.FloatField(default=0) 

    # Donor Eligibility
    eligibility_status = models.CharField(max_length=20, choices=[('Eligible', 'Eligible'), ('Deferred', 'Deferred'),
                                                                  ('Restricted', 'Restricted')],
                                          default='Eligible')
    eligibility_reason = models.TextField(blank=True)

   

    preferred_center = models.ForeignKey(DonationCenter, on_delete=models.DO_NOTHING, null=True, blank=True)
    preferred_times = models.TextField(blank=True)

    # Notifications
    receive_notifications = models.BooleanField(default=True)
    opt_in_communication = models.BooleanField(default=True)

    # Consent and Agreements
    consent_share_information = models.BooleanField(default=False)
    terms_and_conditions_acknowledged = models.BooleanField(default=False)

    # Additional Notes
    additional_notes = models.TextField(blank=True)

    def __str__(self):
        return f"DonorProfile - {self.user_profile.user.username}" 
    

 # next Donation eligibility date
    def eligibilityDate(self):
        last_donation_date = self.last_donation_date
        next_eligibility_date = last_donation_date + timedelta(weeks=8)
        return next_eligibility_date

# TODO Notification or reminders table
# TODO Add next donation next eligible date to blood donor profile table ✅
# TODO Donation history table with one-to-many relationship with Donor profile table ✅