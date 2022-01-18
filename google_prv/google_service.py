# TL;DR - This module creates the Google Drive service

import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_prv.google_auth import generate_credentials


def drive_service():
    try:
        # We create the Drive V3 service and return it
        service = build('drive', 'v3', credentials=generate_credentials())
        logging.info('Google Drive service created successfully')
        return service
    except HttpError as error:
        # Just a few examples of the errors we can handle
        if error.resp.status == 500:
            logging.error("G Suite backend error: {error}")
        elif error.resp.status == 503:
            logging.error("G Suite service unavailble: {error}")
        else:
            logging.error("Unexpected error with Google API: {error}")
