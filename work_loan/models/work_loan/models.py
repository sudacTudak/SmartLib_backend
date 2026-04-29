from django.db import models
from uuid import uuid4 as uuid

from works.models import WorkItem
from common_core.date_utils import get_future_from_today_date
from library.models import LibraryBranch
from users.models import CustomUser
from work_loan.enums import WorkLoanStatus

from .manager import WorkLoanManagerType, WorkLoanManager

__all__ = ['WorkLoan']


class WorkLoan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid, editable=False)
    work_item: WorkItem = models.ForeignKey(WorkItem, related_name='loans', on_delete=models.PROTECT)
    work_item_id: str | None
    library_branch: LibraryBranch = models.ForeignKey(LibraryBranch, related_name='work_loans', on_delete=models.PROTECT)
    library_branch_id: str | None
    client: CustomUser = models.ForeignKey(CustomUser, related_name='work_loans', null=True, blank=True, on_delete=models.SET_NULL)
    client_id: str | None
    created_by: CustomUser = models.ForeignKey(
        CustomUser,
        related_name='created_work_loans',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    created_by_id: str | None
    client_phone = models.CharField(max_length=30)
    client_email = models.EmailField(null=True, blank=True)
    client_fullname = models.CharField(max_length=50)
    loaned_till = models.DateField(default=get_future_from_today_date)
    status = models.PositiveIntegerField(choices=WorkLoanStatus.as_django_model_choices(), default=WorkLoanStatus.Open)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: WorkLoanManagerType = WorkLoanManager()

    class Meta:
        db_table = 'work_loan'
        ordering = ('updated_at', 'created_at', 'closed_at',)

