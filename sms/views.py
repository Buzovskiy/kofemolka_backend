import random

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SmsCodesSerializer
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .turbosms import send_sms
from .models import SmsCodes


@api_view(['POST'])
def send_sms_view(request, api_token):
    # v1/users/send-sms/api_token=qqq
    if api_token != settings.API_TOKEN:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    post_data = request.data.dict()
    sms_code = str(random.randint(1000, 9999))  # make 4 digits sms code
    serializer = SmsCodesSerializer(data={**post_data, 'sms_code': sms_code})

    if serializer.is_valid():
        if 'app_hash' in post_data:
            message = "{}: {}\n {}".format(_('Your code is'), sms_code, post_data['app_hash'])
        else:
            message = sms_code

        turbosms_response = send_sms(message=message, recipients=[serializer.validated_data['phone_number']])
        if turbosms_response.status_code != 200:
            Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_sms_code(request, api_token):
    # v1/users/check-sms-code/api_token=qqq?phone_number=380XXXXXXXXX&sms_code=XXXX
    if api_token != settings.API_TOKEN:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    params = request.query_params.dict()
    if 'phone_number' not in params or 'sms_code' not in params:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    sms_code_instance = SmsCodes.objects.filter(phone_number=params['phone_number']).order_by('-created').first()
    if sms_code_instance is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if sms_code_instance.sms_code == params['sms_code']:
        sms_code_instance.verified = True
        sms_code_instance.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
