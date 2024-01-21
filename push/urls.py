from django.urls import path
from .views import send_test, webhook_test


urlpatterns = [
    path('send-test/', send_test),
    path('webhook-test/', webhook_test),
]
