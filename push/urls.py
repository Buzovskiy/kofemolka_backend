from django.urls import path
from .views import send_test, poster_webhook, add_service_quality_answer


urlpatterns = [
    path('send-test/', send_test),
    path('poster-webhook/', poster_webhook),
    path('ServiceQualityAnswer.Add/api_token=<str:api_token>', add_service_quality_answer)
]
