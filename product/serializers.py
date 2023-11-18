from rest_framework import serializers
from .models import Products, BatchTickets


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'product_name', 'product_id', 'description']


class BatchTicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchTickets
        fields = ['id', 'product_name', 'product_id', 'description']
