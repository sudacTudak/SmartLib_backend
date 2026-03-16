from django.db import models

from .constants import POSITION_NAME_MAX_LENGTH
from uuid import uuid4 as uuid

class StaffPosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid, editable=False)
    name = models.CharField(max_length=POSITION_NAME_MAX_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff_position'
        ordering = ('created_at',)
