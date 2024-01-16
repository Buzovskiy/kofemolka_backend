from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import AppSettingsSerializer
from .models import AppSettings
from delivery.models import DeliveryType
from location.models import Location
from payment.models import PaymentType


@api_view(['GET'])
def get_settings(request, api_token):
    # v1/appsettings/get-settings/api_token=qqq?key=XXXX
    if api_token != settings.API_TOKEN:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    params = request.query_params.dict()
    if 'key' not in params:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        app_settings = AppSettings.objects.filter(key=params['key']).get()
    except AppSettings.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = AppSettingsSerializer(app_settings)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_settings_list(request, api_token):
    # v1/appsettings/get-settings-list/api_token=qqq
    if api_token != settings.API_TOKEN:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    app_settings = AppSettings.objects.all()

    serializer = AppSettingsSerializer(app_settings, many=True)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
def get_company_info(request, api_token):
    # v1/appsettings/get-company-info/api_token=qqq
    # todo: this module needs refactoring according to DRF lib
    if api_token != settings.API_TOKEN:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    data = {
        'settings': {},
        'payment_types': [],
        'delivery_types': [],
        'locations': [],
    }

    for item in AppSettings.objects.all():
        data['settings'][item.key] = item.value

    data['payment_types'] = [{'title': item.title} for item in PaymentType.objects.all()]

    data['delivery_types'] = [{'title': item.title} for item in DeliveryType.objects.all()]

    for location in Location.objects.prefetch_related('locationimage_set').prefetch_related('locationaddress_set'):
        location_data = {
            'id': location.id,
            'spot_id': location.spot_id,
            'name': location.name,
            'spot_name': location.spot_name,
            'spot_address': location.spot_address,
            'region_id': location.region_id,
            'lat': location.lat,
            'lng': location.lng,
            # 'image': location.get_absolute_image_url,
            'wayforpay_key': location.wayforpay_key,
            'wayforpay_account': location.wayforpay_account,
            'location_addresses': [],
            'location_images': [],
        }
        for location_address in location.locationaddress_set.all():
            location_data['location_addresses'].append({'address': location_address.address})

        for location_image in location.locationimage_set.all():
            location_data['location_images'].append({
                'image_url': location_image.get_absolute_image_url,
                'id': location_image.id
            })

        data['locations'].append(location_data)

    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
