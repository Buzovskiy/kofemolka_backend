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
