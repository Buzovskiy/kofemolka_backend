from rest_framework import serializers
from .models import ServiceQualityAnswers, MessageClient


class ServiceQualityAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceQualityAnswers
        fields = ['location', 'client', 'id_clean', 'id_products_quality', 'id_service_quality', 'comment']


class ServiceQualityAnswersSerializerAPI(serializers.Serializer):
    client_id = serializers.IntegerField(required=True)  # client id in poster
    spot_id = serializers.IntegerField(required=True)  # spot id in poster
    id_clean = serializers.IntegerField(required=False)
    id_products_quality = serializers.IntegerField(required=False)
    id_service_quality = serializers.IntegerField(required=False)
    comment = serializers.CharField(required=False, allow_blank=True)


class MessageClientSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(source='client.client_id')

    class Meta:
        model = MessageClient
        fields = ['id', 'type', 'client', 'client_id', 'title', 'body', 'image', 'created_at']
