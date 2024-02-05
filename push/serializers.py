from rest_framework import serializers
from .models import ServiceQualityAnswers


class ServiceQualityAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceQualityAnswers
        fields = ['location', 'clients', 'id_clean', 'id_products_quality', 'id_service_quality', 'comment']
