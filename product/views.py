from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import ProductsSerializer, BatchTicketsSerializer
from .models import Products, BatchTickets
from .exchange import import_products, import_batchtickets


@api_view(['GET'])
def get_products_list(request, api_token):
    # v1/products/get-products/api_token=qqq?type=(products|batchtickets)
    if api_token != settings.API_TOKEN:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    params = request.query_params.dict()
    if 'type' not in params:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if params['type'] not in ['products', 'batchtickets']:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    objects = None
    if params['type'] == 'products':
        objects = Products.objects.all()
    elif params['type'] == 'batchtickets':
        objects = BatchTickets.objects.all()

    objects_serializer = ProductsSerializer(objects, many=True)

    return JsonResponse(objects_serializer.data, status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
def get_product(request, product_id, api_token):
    # v1/product/get-product/product_id/api_token=qqq
    if api_token != settings.API_TOKEN:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        product = Products.objects.filter(product_id=product_id).get()
    except Products.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = ProductsSerializer(product)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_batch_ticket(request, product_id, api_token):
    # v1/product/get-batchticket/product_id/api_token=qqq
    if api_token != settings.API_TOKEN:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        product = BatchTickets.objects.filter(product_id=product_id).get()
    except Products.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = BatchTicketsSerializer(product)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def products_exchange(request, api_token):
    # v1/product/products-exchange/api_token=qqq
    if api_token != settings.API_TOKEN:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    products_created = import_products()
    batchtickets_created = import_batchtickets()
    data = {
        'products_created': products_created['objects_created'],
        'batchtickets_created': batchtickets_created['objects_created']
    }
    return JsonResponse(data=data, status=status.HTTP_200_OK)
