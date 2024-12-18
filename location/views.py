from rest_framework.generics import RetrieveAPIView
from .models import Location
from .serializers import LocationSerializer
from kofemolka_backend.utils import validate_api_token
from django.conf import settings


class LocationDetailView(RetrieveAPIView):
    queryset = Location.objects.prefetch_related('locationaddress_set')\
        .prefetch_related('locationimage_set')
    serializer_class = LocationSerializer
    lookup_field = 'spot_id'

    def get(self, request, *args, **kwargs):
        auth_response = validate_api_token(request, settings.API_TOKEN)
        if auth_response:
            return auth_response  # Return 401 if the token is invalid
        return super().get(request, *args, **kwargs)
