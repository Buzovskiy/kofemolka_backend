from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import AppSettingsSerializer
from .models import AppSettings


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
