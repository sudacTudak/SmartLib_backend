from django.db.models.fields import CharField
from rest_framework import serializers

from amenity.models import Amenity, AmenityVendor
from library.models import LibraryBranch
from .amenity_vendor import AmenityVendorReadSerializer

__all__ = [
    'AmenityReadSerializer',
    'AmenityWriteSerializer',
]





class AmenityReadSerializer(serializers.ModelSerializer):
    library_branch_id = serializers.UUIDField(read_only=True)
    vendor_id = serializers.UUIDField(read_only=True)
    vendor = AmenityVendorReadSerializer(read_only=True)
    vendor_name = serializers.CharField(source='vendor.vendor_name')
    amenity_name = serializers.CharField(source='vendor.amenity_name')

    class Meta:
        model = Amenity
        fields = ('id', 'library_branch_id', 'vendor_id', 'vendor', 'preview_link', 'created_at')
        read_only_fields = fields


class AmenityWriteSerializer(serializers.ModelSerializer):
    library_branch_id = serializers.PrimaryKeyRelatedField(
        queryset=LibraryBranch.objects.all(),
        source='library_branch',
    )
    vendor_id = serializers.PrimaryKeyRelatedField(
        queryset=AmenityVendor.objects.all(),
        source='vendor',
    )

    class Meta:
        model = Amenity
        fields = ('id', 'library_branch_id', 'vendor_id', 'preview_link', 'created_at')
        read_only_fields = ('id', 'created_at')
