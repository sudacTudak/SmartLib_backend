from django.db import models

from library.models import LibraryBranch
from positions.models import Position
from users.models import CustomUser

from uuid import uuid4 as uuid


class StaffProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid, editable=False)
    user = models.OneToOneField(CustomUser, related_name='staff_profile', on_delete=models.CASCADE)
    library_branch = models.ForeignKey(LibraryBranch, related_name='staff', on_delete=models.PROTECT)
    position = models.ForeignKey(Position, related_name='staff', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff_profile'
        ordering_by = ('created_at', )
