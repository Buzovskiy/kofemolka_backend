from django.test import TestCase, SimpleTestCase
from sms.utils import send_message_ping


class SmsTestCase(SimpleTestCase):

    def test_message_ping(self):
        response = send_message_ping()
        self.assertEqual('PONG', response.json()['response_status'])
