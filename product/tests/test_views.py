from django.test import TestCase, Client
from django.conf import settings
from product.exchange import import_products, import_batchtickets
from app_settings.models import AppSettings


API_TOKEN = settings.API_TOKEN


class ProductsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        obj = AppSettings(title='title', key='poster_token', value=settings.POSTER_TOKEN)
        obj.save()

    def test_get_products_list_exists(self):
        data = {'type': 'products'}
        response = self.client.get(f'/v1/products/get-products-list/api_token={API_TOKEN}', data=data)
        self.assertEqual(response.status_code, 200)

    def test_get_batchtickets_list_exists(self):
        data = {'type': 'batchtickets'}
        response = self.client.get(f'/v1/products/get-products-list/api_token={API_TOKEN}', data=data)
        self.assertEqual(response.status_code, 200)

