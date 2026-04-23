from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from library.models import LibraryBranch

__all__ = ['LibraryBranchFeedback']


class LibraryBranchFeedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    library_branch = models.ForeignKey(LibraryBranch, related_name='feedbacks', on_delete=models.CASCADE)
    library_branch_id: str
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='library_branch_feedbacks',
        on_delete=models.CASCADE,
    )
    client_id: str
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'library_branch_feedback'
        ordering = ('-created_at',)
        constraints = (
            models.UniqueConstraint(
                fields=('library_branch', 'client'),
                name='uniq_library_branch_feedback_per_client',
            ),
        )

    def __str__(self) -> str:
        return f'LibraryBranchFeedback({self.library_branch_id}, {self.client_id}, {self.score})'
