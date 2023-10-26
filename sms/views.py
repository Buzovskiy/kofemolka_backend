import random

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SmsCodesSerializer


@api_view(['POST'])
def send_sms_view(request):
    # v1/users/send-sms

    serializer = SmsCodesSerializer(data={**request.data.dict(), 'sms_code': '1234'})
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(data={})


@api_view(['GET', 'POST'])
def sms_view(request):
    # if request.method == 'GET':
    #     # snippets = Snippet.objects.all()
    #     # serializer = SnippetSerializer(snippets, many=True)
    #     # return Response(serializer.data)
    #     pass
    #
    # elif request.method == 'POST':
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    pass
