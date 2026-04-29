from django.db import models

from works.models import Work
from typing import cast

from library.models import LibraryBranch
from uuid import uuid4 as uuid

__all__ = ['WorkItem', ]


class WorkItem(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid)
    library_branch = models.ForeignKey(LibraryBranch, related_name='work_items', on_delete=models.PROTECT)
    work = models.ForeignKey(Work, related_name='work_items', on_delete=models.PROTECT)
    total_count = models.PositiveIntegerField()
    available_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('library_branch', 'work', 'id',)
        db_table = 'work_item'
        constraints = [
            models.UniqueConstraint(
                fields=['work', 'library_branch', ],
                name='unique_book_basis_per_library_branch'
            )
        ]

    def __str__(self):
        work = cast(Work, self.work)
        return work.title

