from django.db import models
from uuid import uuid4 as uuid


class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid)
    name = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'suppliers'
        ordering = ('created_at',)
