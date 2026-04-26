from django.db import models
from uuid import uuid4 as uuid

from amenity.models.amenity.manager import AmenityManager, AmenityManagerType
from library.models import LibraryBranch
from amenity.models.amenity_vendor.model import AmenityVendor
from amenity.storage_paths import AmenityPreviewUploadPath

__all__ = ['Amenity']


class Amenity(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid)
    library_branch = models.ForeignKey(LibraryBranch, related_name='amenities', on_delete=models.PROTECT)
    library_branch_id: str
    vendor = models.ForeignKey(AmenityVendor, related_name='amenities', on_delete=models.PROTECT)
    vendor_id: str
    preview_link = models.ImageField(upload_to=AmenityPreviewUploadPath(), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    objects: AmenityManagerType = AmenityManager()

    class Meta:
        db_table = 'amenity'
        ordering = ('created_at',)