from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .messaging import _send_fcm_message


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
        return Response('post: webhook_test', status=200)
