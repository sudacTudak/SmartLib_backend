from rest_framework import serializers

from amenity.models import Amenity, AmenityVendor
from library.models import LibraryBranch

__all__ = [
    'AmenityVendorReadSerializer',
    'AmenityReadSerializer',
    'AmenityWriteSerializer',
]


class AmenityVendorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityVendor
        fields = ('id', 'amenity_name', 'vendor_name', 'preview_link', 'created_at')
        read_only_fields = fields


class AmenityReadSerializer(serializers.ModelSerializer):
    library_branch_id = serializers.UUIDField(read_only=True)
    vendor_id = serializers.UUIDField(read_only=True)
    vendor = AmenityVendorReadSerializer(read_only=True)

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
