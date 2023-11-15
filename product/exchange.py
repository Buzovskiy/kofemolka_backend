import requests
from .models import Products, BatchTickets


def import_products():
    response = requests.get(url='')
