import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from donations.models import UserToken
from pathlib import Path
from environ import environ



# defining the path of the env file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = f"{BASE_DIR}/keys/.env"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# reading the env file from the file path
environ.Env.read_env(env_file=ENV_PATH)





# this is a function that create the service with which we connect to the Google calendar API to access user's
# resources and perform operations
def create_service(user):
    """
    Creates a service for interacting with the Google Calendar API using the user's credentials.

    Args:
        user: The user for whom the service is being created.

    Returns:
        An instance of the service for interacting with the Google Calendar API.
    """
    # defining the scope of the service 
    credentials = None
    scope = 'https://www.googleapis.com/auth/calendar'

    #importing the required environmental variables
    client_id = env('CLIENT_ID')
    client_secret = env('CLIENT_SECRET')

    # We retrieve user access token and refresh token from the UserToken Model
    user_token = UserToken.objects.get(user=user)
    credentials = Credentials(user_token.access_token, refresh_token=user_token.refresh_token,
                              token_uri='https://oauth2.googleapis.com/token', client_id= client_id,
                              client_secret= client_secret)

    # if the credentials is none or not valid, we try to use refresh token to get a new access token. If it is none,
    # we request for the user authorize the application again.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('Credentials.json', scope)
            credentials = flow.run_local_server(port=0)

        user_token.access_token = credentials.token
        user_token.refresh_token = credentials.refresh_token
        user_token.save()

    # build the service that connects to the Google calendar API
    try:
        service = build('calendar', 'v3', credentials=credentials)
        return service
    # returns a 404 error if it fails
    except HttpError as error:
        print(f'an error occurred: {error}')