from rest_framework import serializers
from .models import SmsCodes


class SmsCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsCodes
        fields = ['phone_number', 'sms_code']
