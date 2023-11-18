from app_settings.poster import Poster
from .models import Products, BatchTickets


def import_products():
    response = Poster().get(url='/api/menu.getProducts', params={'type': 'products'})

    if 'response' not in response.json():
        return {}

    objects_created = 0

    for product in response.json()['response']:
        product_defaults = {
            'product_id': product['product_id'],
            'product_name': product['product_name']
        }
        obj, created = Products.objects.update_or_create(product_id=product['product_id'], defaults=product_defaults)
        if created:
            objects_created += 1
    return {'objects_created': objects_created}


def import_batchtickets():
    response = Poster().get(url='/api/menu.getProducts', params={'type': 'batchtickets'})

    if 'response' not in response.json():
        return {}

    objects_created = 0

    for product in response.json()['response']:
        product_defaults = {
            'product_id': product['product_id'],
            'product_name': product['product_name']
        }
        obj, created = BatchTickets.objects.update_or_create(product_id=product['product_id'],
                                                             defaults=product_defaults)
        if created:
            objects_created += 1
    return {'objects_created': objects_created}
