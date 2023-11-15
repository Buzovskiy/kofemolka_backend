import requests
from json import dumps
from django.test import TestCase, Client
from django.conf import settings
from app_settings.models import AppSettings
from app_settings.poster import Poster


class PosterTestCase(TestCase):

    def setUp(self):
        obj = AppSettings(title='title', key='poster_token', value=settings.POSTER_TOKEN)
        obj.save()
        self.poster_token = obj.value
        self.client = Client()

    def test_poster_token_is_correct(self):
        request_params = {'token': self.poster_token}
        response = requests.get('https://joinposter.com/api/menu.getCategories', request_params)
        msg = response.json()['error'] if 'error' in response.json() else ''
        self.assertFalse('error' in response.json(), msg=msg)

    def test_poster_get_request(self):
        response = Poster().get('/api/menu.getProducts', params={'type': 'products'})
        self.assertFalse('error' in response.json())
