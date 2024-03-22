import random
from smtplib import SMTPException

from django.core.mail import send_mail, EmailMessage

# from twilio.rest import Client
# from wedding.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN


from django.core.mail import send_mail
from django.core.exceptions import ValidationError


def send_email(email, activation_key):
    print("Sending email")
    try:
        result = send_mail('Activation Mail', 'Here is your activation key: ' + activation_key,
                           'EmmanuelNiyi@pulsepoint.world', [email], fail_silently=False)
        print(result)
        return True
    except SMTPException as e:
        raise ValidationError(f"An error occurred while sending the activation email: {e}")
    except Exception as e:
        raise ValidationError(f"An unexpected error occurred while sending the activation email: {e}")

# def send_sms(phone, activation_key):
#     print("am here")
#     account_id = TWILIO_ACCOUNT_SID
#     auth_token = TWILIO_AUTH_TOKEN
#     client = Client(account_id, auth_token)
#
#     message = client.messages.create(
#         body='Hi there! your activation code is ' + activation_key,
#         from_='+18036102363',
#         to=phone
#     )
#
#     print(message.sid)


def generate_activation():
    res = ""
    for _ in range(1, 6):
        x = random.randint(1, 10)
        res = res + str(x)
    return res
