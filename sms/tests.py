from django.test import TestCase, SimpleTestCase
from django.core.exceptions import ValidationError
import decouple
from .turbosms import Turbosms
from .models import Setting, validate_phone_is_ukrainian
from .serializers import SmsCodesSerializer


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


class ValidateUkrainianPhoneNumberTestCase(SimpleTestCase):
    def test_number(self):
        self.assertRaises(ValidationError, validate_phone_is_ukrainian, '480986260636')
        self.assertRaises(ValidationError, validate_phone_is_ukrainian, '+380986260636')
        self.assertRaises(ValidationError, validate_phone_is_ukrainian, '3809862606360')
        try:
            validate_phone_is_ukrainian('380986260636')
        except ValidationError:
            self.fail("validate_phone_is_ukrainian('380986260636') raised ValidationError unexpectedly!")


class SerializerTestCase(SimpleTestCase):
    def test_sms_codes_serializer(self):
        serializer = SmsCodesSerializer(data={'phone_number': '+380986260636', 'sms_code': '1234'})
        self.assertEqual(False, serializer.is_valid())
        serializer = SmsCodesSerializer(data={'phone_number': '380986260636', 'sms_code': '1234'})
        self.assertEqual(True, serializer.is_valid())
