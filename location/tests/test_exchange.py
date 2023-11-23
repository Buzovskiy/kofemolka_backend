from django.test import TestCase
from django.conf import settings
from app_settings.models import AppSettings
from app_settings.poster import Poster
from location.exchange import import_locations
from location.models import Location


class ImportLocationsTestCase(TestCase):

    def setUp(self):
        obj = AppSettings(title='title', key='poster_token', value=settings.POSTER_TOKEN)
        obj.save()

    def test_create_products(self):
        """Check if locations count in API is equal to count in database after create"""
        response = Poster().get(url='/api/access.getSpots')
        count_in_api = len(response.json()['response'])
        import_locations()
        count_in_db = Location.objects.all().count()
        self.assertEqual(count_in_api, count_in_db)
