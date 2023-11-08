from django.shortcuts import render


# @api_view(['GET'])
# def check_sms_code(request, api_token):
#     # v1/users/check-sms-code/api_token=qqq?phone_number=380XXXXXXXXX&sms_code=XXXX
#     if api_token != settings.API_TOKEN:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#
#     params = request.query_params.dict()
#     if 'phone_number' not in params or 'sms_code' not in params:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     sms_code_instance = SmsCodes.objects.filter(phone_number=params['phone_number']).order_by('-created').first()
#     if sms_code_instance is None:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     if sms_code_instance.sms_code == params['sms_code']:
#         sms_code_instance.verified = True
#         sms_code_instance.save()
#         return Response(status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)
