from django.test import TestCase, Client
from django.conf import settings
from app_settings.models import AppSettings


API_TOKEN = settings.API_TOKEN


class GetSettingsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_wrong_token(self):
        response = self.client.get(f'/v1/appsettings/get-settings/api_token=wrong_token')
        self.assertEqual(response.status_code, 401)

    def test_param_does_not_exists(self):
        response = self.client.get(f'/v1/appsettings/get-settings/api_token={API_TOKEN}')
        self.assertEqual(response.status_code, 400)

    def test_object_does_not_exists(self):
        data = {'key': 'token_key'}
        response = self.client.get(f'/v1/appsettings/get-settings/api_token={API_TOKEN}', data=data)
        self.assertEqual(response.status_code, 400)

    def test_object_exists(self):
        obj = AppSettings(title='title', key='token_key', value='token value')
        obj.save()
        data = {'key': 'token_key'}
        response = self.client.get(f'/v1/appsettings/get-settings/api_token={API_TOKEN}', data=data)
        self.assertEqual(response.status_code, 200)


class GetSettingsListTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_wrong_token(self):
        response = self.client.get(f'/v1/appsettings/get-settings-list/api_token=wrong_token')
        self.assertEqual(response.status_code, 401)

    def test_get_settings_list(self):
        obj = AppSettings(title='title', key='token_key', value='token value')
        obj.save()
        response = self.client.get(f'/v1/appsettings/get-settings-list/api_token={API_TOKEN}')
        self.assertEqual(response.status_code, 200)
