from django.db import models
from uuid import uuid4 as uuid


__all__ = ['AmenityVendor']

class AmenityVendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid, editable=False)
    amenity_name = models.CharField(max_length=50)
    preview_link = models.CharField(blank=True)
    vendor_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'amenity_vendor'
        ordering = ('created_at',)

