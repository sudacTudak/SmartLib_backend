from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from works.models import Work

__all__ = ['WorkFeedback']


class WorkFeedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    work = models.ForeignKey(Work, related_name='feedbacks', on_delete=models.CASCADE)
    work_id: str
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='work_feedbacks',
        on_delete=models.CASCADE,
    )
    client_id: str
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'work_feedback'
        ordering = ('-created_at',)
        constraints = (
            models.UniqueConstraint(fields=('work', 'client'), name='uniq_book_basis_feedback_per_client'),
        )

    def __str__(self) -> str:
        return f'WorkFeedback({self.work_id}, {self.client_id}, {self.score})'
