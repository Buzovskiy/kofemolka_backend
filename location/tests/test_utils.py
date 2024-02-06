from django.test import TestCase
from django.conf import settings
from location.utils import get_location_or_create
from app_settings.poster import Poster
from app_settings.models import AppSettings


class TestUtils(TestCase):
    def setUp(self):
        obj = AppSettings(title='title', key='poster_token', value=settings.POSTER_TOKEN)
        obj.save()

    def test_get_location_or_create(self):
        response = Poster().get(url='/api/access.getSpots')
        locations = response.json()['response']
        if len(locations):
            location_remote = locations[0]
            location = get_location_or_create(location_remote['spot_id'])
            self.assertFalse(location is None)

        location = get_location_or_create(999999999)
        self.assertTrue(location is None)
