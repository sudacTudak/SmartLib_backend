from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from books_model.models import BookBasis

__all__ = ['BookBasisFeedback']


class BookBasisFeedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    book_basis = models.ForeignKey(BookBasis, related_name='feedbacks', on_delete=models.CASCADE)
    book_basis_id: str
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='book_basis_feedbacks',
        on_delete=models.CASCADE,
    )
    client_id: str
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'book_basis_feedback'
        ordering = ('-created_at',)
        constraints = (
            models.UniqueConstraint(fields=('book_basis', 'client'), name='uniq_book_basis_feedback_per_client'),
        )

    def __str__(self) -> str:
        return f'BookBasisFeedback({self.book_basis_id}, {self.client_id}, {self.score})'
