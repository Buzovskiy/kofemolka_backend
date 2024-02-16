from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from .messaging import _send_fcm_message
from .serializers import ServiceQualityAnswersSerializer, ServiceQualityAnswersSerializerAPI, MessageClientSerializer
from django.conf import settings
from clients.utils import get_client_or_create
from location.utils import get_location_or_create
from app_settings.poster import Poster
from order.models import Transaction
from .models import MessageClient


@api_view(['GET', 'POST'])
def send_test(request):
    if request.method == 'GET':
        return Response('my response get')
    if request.method == 'POST':
        push_data = request.data
        resp = _send_fcm_message(push_data)
        return Response(resp.text, status=resp.status_code)


@api_view(['GET', 'POST'])
def poster_webhook(request):
    if request.method == 'GET':
        return Response('get: webhook_test')
    if request.method == 'POST':
        try:
            if request.data['object'] == 'transaction' and request.data['action'] == 'closed':
                transaction_id = request.data['object_id']
                response = Poster().get(url='/api/dash.getTransaction', params={'transaction_id': transaction_id})
                if not len(response.json()['response']):
                    return Response(status=200)
                transaction = response.json()['response'][0]
                client_id = transaction['client_id']
                spot_id = transaction['spot_id']
                transaction_id = transaction['transaction_id']
                client = get_client_or_create(client_id)
                location = get_location_or_create(spot_id)
                if not (client and location):
                    return Response(status=200)
                # Save the information about the client order.
                Transaction.objects.update_or_create(
                    transaction_id=transaction_id,
                    defaults={"transaction_id": transaction_id, "client": client, "location": location},
                )
        except KeyError:
            pass
        return Response(status=200)


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


class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class ClientMessagesHistoryView(generics.ListAPIView):
    serializer_class = MessageClientSerializer
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        client_id = self.request.query_params.get('client_id')
        queryset = MessageClient.objects.filter(client__client_id=client_id).order_by('-created_at')
        return queryset

    def get(self, request, *args, **kwargs):
        api_token = kwargs.get('api_token')
        if api_token != settings.API_TOKEN:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.query_params.get('client_id') is None:
            return Response('client_id is not specified', status=status.HTTP_400_BAD_REQUEST)
        return self.list(request, *args, **kwargs)
