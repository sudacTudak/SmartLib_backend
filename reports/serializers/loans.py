from __future__ import annotations

from django.utils import timezone
from rest_framework import serializers

from work_loan.enums import WorkLoanStatus
from work_loan.models import WorkLoan

__all__ = ['WorkLoanIssueReportSerializer']


class WorkLoanIssueReportSerializer(serializers.ModelSerializer):
    library_branch_address = serializers.CharField(source='library_branch.address', read_only=True)
    work_title = serializers.CharField(source='work_item.work.title', read_only=True)
    staff_full_name = serializers.SerializerMethodField()
    client_display = serializers.SerializerMethodField()
    loaned_at = serializers.DateTimeField(source='created_at', read_only=True)
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = WorkLoan
        fields = (
            'id',
            'library_branch_address',
            'work_title',
            'staff_full_name',
            'client_display',
            'loaned_at',
            'loaned_till',
            'is_overdue',
            'status',
        )
        read_only_fields = fields

    @staticmethod
    def _format_user_name(user) -> str:
        if user is None:
            return ''
        parts = [user.last_name, user.first_name, getattr(user, 'patronymic', '') or '']
        return ' '.join(p for p in parts if p).strip()

    def get_staff_full_name(self, loan: WorkLoan) -> str:
        return self._format_user_name(loan.created_by)

    def get_client_display(self, loan: WorkLoan) -> dict[str, str | None]:
        return {
            'full_name': loan.client_fullname,
            'phone': loan.client_phone,
            'email': loan.client_email,
        }

    def get_is_overdue(self, loan: WorkLoan) -> bool:
        if loan.status != WorkLoanStatus.Open:
            return False
        today = timezone.localdate()
        return bool(loan.loaned_till < today)
