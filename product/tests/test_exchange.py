from django.test import TestCase
from django.conf import settings
from app_settings.models import AppSettings
from app_settings.poster import Poster
from product.exchange import import_products, import_batchtickets
from product.models import Products, BatchTickets


class ImportProductsTestCase(TestCase):

    def setUp(self):
        obj = AppSettings(title='title', key='poster_token', value=settings.POSTER_TOKEN)
        obj.save()

    def test_create_products(self):
        """Check if products count in API is equal to count in database after create"""
        response = Poster().get(url='/api/menu.getProducts', params={'type': 'products'})
        count_in_api = len(response.json()['response'])
        import_products()
        count_in_db = Products.objects.all().count()
        self.assertEqual(count_in_api, count_in_db)

    def test_create_batchtickets(self):
        """Check if batchtickets count in API is equal to count in database after create"""
        response = Poster().get(url='/api/menu.getProducts', params={'type': 'batchtickets'})
        count_in_api = len(response.json()['response'])
        import_batchtickets()
        count_in_db = BatchTickets.objects.all().count()
        self.assertEqual(count_in_api, count_in_db)
