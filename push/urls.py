from django.urls import path
from .views import send_test, webhook_test, add_service_quality_answer


urlpatterns = [
    path('send-test/', send_test),
    path('webhook-test/', webhook_test),
    path('ServiceQualityAnswer.Add/api_token=<str:api_token>', add_service_quality_answer)
]
