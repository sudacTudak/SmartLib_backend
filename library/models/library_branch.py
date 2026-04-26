from django.db import models
from uuid import uuid4 as uuid

from library.storage_paths import LibraryPreviewUploadPath

__all__ = ['LibraryBranch', 'LibraryBranchFieldsMeta']

LibraryBranchFieldsMeta = dict(
    ADDRESS_MAX_LENGTH=255,
)


class LibraryBranch(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid)
    address = models.CharField(max_length=LibraryBranchFieldsMeta['ADDRESS_MAX_LENGTH'])
    preview_link = models.ImageField(upload_to=LibraryPreviewUploadPath(), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'library_branch'

    def __str__(self):
        return f'Library: {self.address}'
