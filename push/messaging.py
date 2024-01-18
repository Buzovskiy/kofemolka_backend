"""Server Side FCM sample.

Firebase Cloud Messaging (FCM) can be used to send messages to clients on iOS,
Android and Web.

This sample uses FCM to send two types of messages to clients that are subscribed
to the `news` topic. One type of message is a simple notification message (display message).
The other is a notification message (display notification) with platform specific
customizations. For example, a badge is added to messages that are sent to iOS devices.
"""

import argparse
import json
import requests
import google.auth.transport.requests
from google.oauth2 import service_account
from django.conf import settings

PROJECT_ID = 'vitalii-fecf8'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']


# [START retrieve_access_token]
def _get_access_token():
    """Retrieve a valid access token that can be used to authorize requests.

    :return: Access token.
    """
    credentials = service_account.Credentials.from_service_account_file(
        settings.BASE_DIR / 'push/firebase_private_key.json',
        scopes=SCOPES)
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token


# [END retrieve_access_token]

def _send_fcm_message(fcm_message):
    """Send HTTP request to FCM with given message.

    Args:
      fcm_message: JSON object that will make up the body of the request.
    """
    # [START use_access_token]
    headers = {
        'Authorization': 'Bearer ' + _get_access_token(),
        'Content-Type': 'application/json; UTF-8',
    }
    # [END use_access_token]
    return requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)


def _build_common_message():
    """Construct common notification message.

    Construct a JSON object that will be used to define the
    common parts of a notification message that will be sent
    to any app instance subscribed to the news topic.
    """
    return {
        'message': {
            'token': '',
            'notification': {
                'title': 'Hola!',
                'body': 'Como estas?',
            }
        }
    }


def main():
    specific_device_message = _build_common_message()
    print(json.dumps(specific_device_message, indent=2))
    _send_fcm_message(specific_device_message)


if __name__ == '__main__':
    main()
