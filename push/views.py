from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .messaging import _send_fcm_message
from .serializers import ServiceQualityAnswersSerializer, ServiceQualityAnswersSerializerAPI
from django.conf import settings
from clients.utils import get_client_or_create
from location.utils import get_location_or_create


@api_view(['GET', 'POST'])
def send_test(request):
    if request.method == 'GET':
        return Response('my response get')
    if request.method == 'POST':
        push_data = request.data
        resp = _send_fcm_message(push_data)
        return Response(resp.text, status=resp.status_code)


@api_view(['GET', 'POST'])
def webhook_test(request):
    if request.method == 'GET':
        return Response('get: webhook_test')
    if request.method == 'POST':
        if ('object' in request.data and 'object_id' in request.data and 'action' in request.data and
                request.data['object'] == 'transaction'):
            pass
        return Response('post: webhook_test', status=200)


@api_view(['POST'])
def add_service_quality_answer(request, api_token):
    if request.method == 'POST':
        if api_token != settings.API_TOKEN:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer_api = ServiceQualityAnswersSerializerAPI(data=request.data)
        if not serializer_api.is_valid():
            return Response(serializer_api.errors, status=status.HTTP_400_BAD_REQUEST)
        client = get_client_or_create(client_id=request.data['client_id'])
        location = get_location_or_create(spot_id=request.data['spot_id'])
        if client is None or location is None:
            return Response('Client or location are not found', status=status.HTTP_400_BAD_REQUEST)
        model_data = {
            'client': client.id,
            'location': location.id
        }
        new_request_data = request.data.copy()
        new_request_data.update(model_data)
        serializer = ServiceQualityAnswersSerializer(data=new_request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
