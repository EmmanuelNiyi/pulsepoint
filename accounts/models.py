from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from pulsepoint.settings import AUTH_USER_MODEL


# Create your models here.

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


GENDER_SELECTION = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('NS', 'Not Specified'),
]


class User(AbstractUser):
    roles = models.ManyToManyField(Role, related_name='users')

    def __str__(self):
        return self.email


class UserActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    activation_key = models.CharField(max_length=30, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    contact_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone = models.CharField(max_length=12, default="")
    zip_code = models.CharField(max_length=10, default="")
    local_government = models.CharField(max_length=25, default="")
    state = models.CharField(max_length=255)
    home_address = models.CharField(max_length=255, default="")
    country = models.CharField(max_length=255)

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)


