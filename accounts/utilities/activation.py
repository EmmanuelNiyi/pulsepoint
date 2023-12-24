from django.core.mail import send_mail, EmailMessage


# from twilio.rest import Client
# from wedding.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN


def send_email(email, activation_key):
    # result = EmailMessage(subject='Activation Mail', body='Here is your activation key ' + activation_key,
    #                       to=['emmanuelniyioriolowo@gmail.com'])
    result = send_mail('Activation Mail', 'Here is your activation key ' + activation_key,
                       'emmanuelniyi03@gmial.com', [email], fail_silently=False)
    return result

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
