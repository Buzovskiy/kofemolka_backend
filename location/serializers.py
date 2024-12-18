from rest_framework import serializers
from .models import Location, LocationAddress, LocationImage


class LocationAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationAddress
        fields = [
            'id',
            'address',
        ]


class LocationImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField(source='get_absolute_image_url')

    class Meta:
        model = LocationImage
        fields = [
            'id',
            'image_url',
        ]


class LocationSerializer(serializers.ModelSerializer):
    location_addresses = LocationAddressSerializer(source='locationaddress_set', many=True, read_only=True)
    location_images = LocationImageSerializer(source='locationimage_set', many=True, read_only=True)

    class Meta:
        model = Location
        fields = [
            'id',
            'spot_id',
            'name',
            'spot_name',
            'spot_address',
            'region_id',
            'lat',
            'lng',
            'wayforpay_key',
            'wayforpay_account',
            'location_addresses',
            'location_images'
        ]
