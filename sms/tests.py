from django.test import TestCase, SimpleTestCase
import decouple
from .utils import Turbosms
from .models import Setting


SMS_SIGNATURE = decouple.config('SMS_SIGNATURE')
SMS_TOKEN = decouple.config('SMS_TOKEN')


class SmsTestCase(TestCase):

    def setUp(self):
        Setting.objects.create(
            sms_signature=SMS_SIGNATURE,
            sms_token=SMS_TOKEN,
            active=True,
        )

    def test_message_ping(self):
        sms_settings = Setting.objects.filter(sms_signature=SMS_SIGNATURE).get()
        turbosms_instance = Turbosms(
            sms_token=sms_settings.sms_token,
            sms_signature=sms_settings.sms_signature
        )
        response = turbosms_instance.send_message_ping()
        self.assertEqual('PONG', response.json()['response_status'])
