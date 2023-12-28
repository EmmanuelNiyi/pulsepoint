from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from accounts.models import UserProfile, User
from donations.models import DonorProfile


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    print(f"Creating or updating user profile for {instance}")

    from accounts.models import UserProfile

    # Check if a profile already exists for the user
    existing_profile = UserProfile.objects.filter(user=instance).first()

    if not existing_profile:
        # If no profile exists, create a new one
        UserProfile.objects.create(user=instance)
        print(f"User profile for {instance} created")
    else:
        # If a profile exists, update it or perform any desired actions
        print(f"User profile for {instance} already exists. Updating or performing additional actions.")


@receiver(post_save, sender=UserProfile)
def create_donor_profile(instance, created, **kwargs):
    print(f"Creating or updating donor profile for {instance}")

    # Check if a donor profile already exists for the user profile
    existing_donor_profile = DonorProfile.objects.filter(user_profile=instance).first()

    if not existing_donor_profile:
        # If no donor profile exists, create a new one
        DonorProfile.objects.create(user=instance.user, user_profile=instance)
        print(f"Donor profile for {instance} created")
    else:
        # If a donor profile exists, update it or perform any desired actions
        print(f"Donor profile for {instance} already exists. Updating or performing additional actions.")
