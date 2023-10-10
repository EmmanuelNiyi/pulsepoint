from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


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


class RoleManager(models.Manager):
    def get_users_with_role(self, role_name):
        return self.get(name=role_name).users.all()


class User(AbstractUser):
    roles = models.ManyToManyField(Role, related_name='users')

    def __str__(self):
        return self.email


class Donor(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = RoleManager()

    availability = models.TextField()

    def __str__(self):
        return self.user


class Volunteer(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = RoleManager()

    blood_type = models.CharField(max_length=10)
    contact_info = models.TextField()
    center = models.ForeignKey("DonationCenter", on_delete=models.CASCADE)
    availability = models.TextField()


    def __str__(self):
        return self.user



