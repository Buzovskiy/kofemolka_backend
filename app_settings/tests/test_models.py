from django.test import TestCase
from django.conf import settings
from app_settings.models import AppSettings


class AppSettingsTestCase(TestCase):

    def setUp(self):
        obj = AppSettings(title='title', key='poster_token', value=settings.POSTER_TOKEN)
        obj.save()

    def test_poster_manager(self):
        count = AppSettings.poster_token.all().count()
        self.assertEqual(1, count)
