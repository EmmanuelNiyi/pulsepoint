# Generated by Django 3.2.22 on 2023-12-21 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='user',
        ),
        migrations.DeleteModel(
            name='Donor',
        ),
        migrations.DeleteModel(
            name='Volunteer',
        ),
    ]
