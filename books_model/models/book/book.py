from django.db import models

from books_model.models import BookBasis
from typing import cast

from library.models import LibraryBranch
from uuid import uuid4 as uuid

__all__ = ['Book', ]


class Book(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid)
    library_branch = models.ForeignKey(LibraryBranch, related_name='books', on_delete=models.PROTECT)
    book_basis = models.ForeignKey(BookBasis, related_name='books', on_delete=models.PROTECT)
    total_count = models.PositiveIntegerField()
    available_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('library_branch', 'book_basis', 'id',)
        db_table = 'book'
        constraints = [
            models.UniqueConstraint(
                fields=['book_basis', 'library_branch', ],
                name='unique_book_basis_per_library_branch'
            )
        ]

    def __str__(self):
        basis = cast(BookBasis, self.book_basis)
        return basis.title
