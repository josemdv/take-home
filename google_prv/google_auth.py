# TL;DR - This module handles the authentication with Google
# If a token.json doesn't exist, it will use the method
# run_local_server to open your browser and initiate the OAuth 2.0 flow
# to generate a token.json file used to generate the Google service

from __future__ import print_function

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


import os.path


# If you are modifying these scopes, delete the file token.json.
# Always try to use the scope with the lowest access needed
SCOPES = ['https://www.googleapis.com/auth/drive']


def generate_credentials():
    """This functions checks if a token.json file exists. If it doesn't,
    it will open a web flow to generate one using the existing creds.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials, run local server to create auth.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # Port # can be changed - Using Netflix founding year 1997
            creds = flow.run_local_server(
                host='127.0.0.1',
                port=1997,
                prompt="consent")
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
