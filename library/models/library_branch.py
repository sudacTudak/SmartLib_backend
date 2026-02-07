from django.db import models

__all__ = ['LibraryBranch', 'LibraryBranchFieldsMeta']

LibraryBranchFieldsMeta = dict(
    ADDRESS_MAX_LENGTH = 255,
)

class LibraryBranch(models.Model):
    id = models.BigAutoField(primary_key=True)
    address = models.CharField(max_length=LibraryBranchFieldsMeta['ADDRESS_MAX_LENGTH'])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'library_branch'

    def __str__(self):
        return f'Library: {self.address}'