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
    credentials = None
    scope = 'https://www.googleapis.com/auth/calendar'

    # We retrieve user access token and refresh token from the UserToken Model
    user_token = UserToken.objects.get(user=user)
    credentials = Credentials(user_token.access_token, refresh_token=user_token.refresh_token,
                              token_uri='https://oauth2.googleapis.com/token', client_id= env.CLIENT_ID,
                              client_secret= env.CLIENT_SECRET)

    # if the credentials is none or not valid, we try to use refresh token to get a new access token. If it is none,
    # we request for the user authorize the application again.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('Credentials.json', scope)
            credentials = flow.run_local_server(port=0)
            assert isinstance(credentials, object)

        credentials_json = credentials.to_json()
        user_token.access_token = credentials_json.token
        user_token.refresh_token = credentials_json.refresh_token
        user_token.save()

    # build the service that connects to the Google calendar API
    try:
        service = build('calendar', 'v3', credentials=credentials)
        return service
    # returns a 404 error if it fails
    except HttpError as error:
        print(f'an error occurred: {error}')