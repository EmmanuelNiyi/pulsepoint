# Generated by Django 4.2.1 on 2023-12-24 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location_address', models.CharField(max_length=255)),
                ('location_city', models.CharField(max_length=100)),
                ('location_state', models.CharField(max_length=50)),
                ('location_zipcode', models.CharField(blank=True, max_length=20, null=True)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone', models.CharField(max_length=15)),
                ('accreditation_status', models.CharField(choices=[('Accredited', 'Accredited'), ('Pending', 'Pending Accreditation'), ('Not Accredited', 'Not Accredited')], default='Not Accredited', max_length=50)),
                ('accreditation_date', models.DateField(blank=True, null=True)),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('appointment_availability', models.BooleanField(default=False)),
                ('appointment_scheduling_system', models.CharField(blank=True, max_length=100, null=True)),
                ('notification_preferences', models.CharField(blank=True, max_length=100)),
                ('additional_notes', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('availability_days_times', models.TextField()),
                ('preferred_roles', models.CharField(blank=True, max_length=100)),
                ('volunteer_status', models.CharField(blank=True, max_length=100)),
                ('volunteer_hours_logged', models.PositiveIntegerField(default=0)),
                ('certification_status', models.CharField(choices=[('Certified', 'Certified'), ('Not Certified', 'Not Certified')], default='Not Certified', max_length=50)),
                ('training_completion_dates', models.DateField(blank=True, null=True)),
                ('communication_preferences', models.CharField(blank=True, max_length=100)),
                ('volunteer_shift_notifications', models.BooleanField(default=True)),
                ('consent_share_information', models.BooleanField(default=False)),
                ('acknowledgment_of_policies', models.BooleanField(default=False)),
                ('additional_notes', models.TextField(blank=True)),
                ('verification_status', models.CharField(choices=[('Pending', 'Pending'), ('Verified', 'Verified')], default='Pending', max_length=50)),
                ('date_of_verification', models.DateField(blank=True, null=True)),
                ('affiliated_donation_centers', models.ManyToManyField(related_name='volunteers', to='donations.donationcenter')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
