from django.urls import path
from .views import LocationDetailView


urlpatterns = [
    path('<str:spot_id>/', LocationDetailView.as_view(), name='location-detail'),
]
