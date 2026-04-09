from django.db import models
from uuid import uuid4 as uuid
from books_model.models import Book
from common_core.date_utils import get_future_from_today_date
from library.models import LibraryBranch
from users.models import CustomUser
from book_loan.enums import BookLoanStatus
from .manager import BookLoanManagerType, BookLoanManager

__all__ = ['BookLoan']

class BookLoan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid, editable=False)
    book: Book = models.ForeignKey(Book, related_name='loans', on_delete=models.PROTECT)
    book_id: str | None
    library_branch: LibraryBranch = models.ForeignKey(LibraryBranch, related_name='book_loans', on_delete=models.PROTECT)
    library_branch_id: str | None
    client: CustomUser = models.ForeignKey(CustomUser, related_name='book_loans', null=True, blank=True, on_delete=models.SET_NULL)
    client_id: str | None
    created_by: CustomUser = models.ForeignKey(
        CustomUser,
        related_name='created_book_loans',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    created_by_id: str | None
    client_phone = models.CharField(max_length=30)
    client_email = models.EmailField(null=True, blank=True)
    client_fullname = models.CharField(max_length=50)
    loaned_till = models.DateField(default=get_future_from_today_date)
    status = models.PositiveIntegerField(choices=BookLoanStatus.as_django_model_choices(), default=BookLoanStatus.Open)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: BookLoanManagerType = BookLoanManager()

    class Meta:
        db_table = 'book_loan'
        ordering = ('updated_at', 'created_at', 'closed_at',)
