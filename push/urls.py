from django.urls import path
from .views import send_test


urlpatterns = [
    path('send-test/', send_test)
]
