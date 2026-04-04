from rest_framework import serializers
from ..models import AmenityVendor

__all__ = ['AmenityVendorReadSerializer', 'AmenityVendorWriteSerializer']


class AmenityVendorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityVendor
        fields = ('id', 'amenity_name', 'vendor_name', 'preview_link', 'created_at')
        read_only_fields = fields


class AmenityVendorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityVendor
        fields = ('amenity_name', 'vendor_name', 'preview_link')
