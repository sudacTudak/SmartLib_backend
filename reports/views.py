from __future__ import annotations

from http import HTTPMethod
from typing import cast

from django.db.models import Count, DateTimeField, OuterRef, QuerySet, Subquery
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from common_core.classes import ViewSetBase
from http_core import HTTPResponse
from inventory_movement.enums import InventoryMovementType
from inventory_movement.models import InventoryMovement
from reports.query_params import ReportQueryParams
from reports.serializers import (
    BranchLoanActivityReportRowSerializer,
    HoldingsInBranchesReportSerializer,
    InventoryMovementFundReportSerializer,
    TopLoanedWorksReportRowSerializer,
    WorkLoanIssueReportSerializer,
)
from users.query_library_scope import scope_library_branch_filters
from users.models import CustomUser
from users.permissions import IsStaff
from work_loan.enums import WorkLoanStatus
from work_loan.models import WorkLoan
from works.models import WorkItem

__all__ = ['ReportsViewSet']

_REPORT_ACTIONS = frozenset({
    'holdings_in_branches',
    'work_loans_issued',
    'work_loans_overdue',
    'inventory_movements',
    'ranking_loaned_works',
    'ranking_branch_loans',
})


class ReportsViewSet(ViewSetBase[QuerySet[WorkItem]], GenericViewSet):
    queryset = WorkItem.objects.none()
    http_method_names = ['get', 'head', 'options']

    def get_permissions(self):
        return [IsStaff()]

    def get_query_params_model_class(self):
        if self.action in _REPORT_ACTIONS:
            return ReportQueryParams
        return None

    def get_queryset(self) -> QuerySet[WorkItem]:
        return WorkItem.objects.none()

    def list(self, request, *args, **kwargs):
        return HTTPResponse.failure(
            message='Укажите конкретный отчёт в URL (см. документацию API).',
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def _params(self) -> ReportQueryParams | None:
        return cast(ReportQueryParams | None, self.get_processed_query_params())

    def _user(self) -> CustomUser:
        return cast(CustomUser, self.request.user)

    def _narrow_branch(self, qs: QuerySet, *, library_branch_lookup: str) -> QuerySet:
        user = self._user()
        params = self._params()
        qs = scope_library_branch_filters(qs, user=user, library_branch_lookup=library_branch_lookup)
        if user.is_admin and params and params.library_branch_id:
            qs = qs.filter(**{library_branch_lookup: str(params.library_branch_id)})
        return qs

    def _apply_loan_dates(self, qs: QuerySet) -> QuerySet:
        params = self._params()
        if params is None:
            return qs
        if params.date_from:
            qs = qs.filter(created_at__date__gte=params.date_from)
        if params.date_to:
            qs = qs.filter(created_at__date__lte=params.date_to)
        return qs

    @action(url_path='holdings-by-branches', detail=False, methods=[HTTPMethod.GET])
    def holdings_in_branches(self, request, *args, **kwargs):
        last_in_sq = (
            InventoryMovement.objects.filter(
                work_id=OuterRef('work_id'),
                library_branch_id=OuterRef('library_branch_id'),
                type=InventoryMovementType.In.value,
            )
            .order_by('-created_at')
            .values('created_at')[:1]
        )
        qs = WorkItem.objects.select_related('library_branch', 'work').annotate(
            last_supply_at=Subquery(last_in_sq, output_field=DateTimeField()),
        )
        qs = self._narrow_branch(qs, library_branch_lookup='library_branch_id')
        qs = qs.order_by('library_branch__address', 'work__title')
        serializer = HoldingsInBranchesReportSerializer(qs, many=True)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

    @action(url_path='work-loans-issued', detail=False, methods=[HTTPMethod.GET])
    def work_loans_issued(self, request, *args, **kwargs):
        qs = WorkLoan.objects.select_related('library_branch', 'work_item__work', 'created_by')
        qs = self._narrow_branch(qs, library_branch_lookup='library_branch_id')
        qs = self._apply_loan_dates(qs)
        params = self._params()
        if not (params and params.include_closed_loans):
            qs = qs.filter(status=WorkLoanStatus.Open)
        qs = qs.order_by('-created_at')
        serializer = WorkLoanIssueReportSerializer(qs, many=True)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

    @action(url_path='work-loans-overdue', detail=False, methods=[HTTPMethod.GET])
    def work_loans_overdue(self, request, *args, **kwargs):
        today = timezone.localdate()
        qs = WorkLoan.objects.select_related('library_branch', 'work_item__work', 'created_by').filter(
            status=WorkLoanStatus.Open,
            loaned_till__lt=today,
        )
        qs = self._narrow_branch(qs, library_branch_lookup='library_branch_id')
        qs = self._apply_loan_dates(qs)
        qs = qs.order_by('loaned_till', 'library_branch__address')
        serializer = WorkLoanIssueReportSerializer(qs, many=True)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

    @action(url_path='inventory-movements', detail=False, methods=[HTTPMethod.GET])
    def inventory_movements(self, request, *args, **kwargs):
        user = self._user()
        qs = InventoryMovement.objects.select_related('library_branch', 'work', 'supplier').order_by('-created_at')
        qs = qs.scoped_for_staff_same_library(user)
        params = self._params()
        if user.is_admin and params and params.library_branch_id:
            qs = qs.filter(library_branch_id=str(params.library_branch_id))
        if params:
            if params.date_from:
                qs = qs.filter(created_at__date__gte=params.date_from)
            if params.date_to:
                qs = qs.filter(created_at__date__lte=params.date_to)
        serializer = InventoryMovementFundReportSerializer(qs, many=True)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

    @action(url_path='ranking-loaned-works', detail=False, methods=[HTTPMethod.GET])
    def ranking_loaned_works(self, request, *args, **kwargs):
        qs = WorkLoan.objects.all()
        qs = self._narrow_branch(qs, library_branch_lookup='library_branch_id')
        qs = self._apply_loan_dates(qs)
        qs = (
            qs.values('work_item__work_id', 'work_item__work__title')
            .annotate(loan_operations_count=Count('id'))
            .order_by('-loan_operations_count', 'work_item__work__title')
        )
        rows = [
            {
                'rank': rank,
                'work_id': row['work_item__work_id'],
                'work_title': row['work_item__work__title'],
                'loan_operations_count': row['loan_operations_count'],
            }
            for rank, row in enumerate(qs, start=1)
        ]
        serializer = TopLoanedWorksReportRowSerializer(rows, many=True)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

    @action(url_path='ranking-branch-loans', detail=False, methods=[HTTPMethod.GET])
    def ranking_branch_loans(self, request, *args, **kwargs):
        qs = WorkLoan.objects.all()
        qs = self._narrow_branch(qs, library_branch_lookup='library_branch_id')
        qs = self._apply_loan_dates(qs)
        qs = (
            qs.values('library_branch_id', 'library_branch__address')
            .annotate(loan_operations_count=Count('id'))
            .order_by('-loan_operations_count', 'library_branch__address')
        )
        rows = [
            {
                'rank': rank,
                'library_branch_id': row['library_branch_id'],
                'library_branch_address': row['library_branch__address'],
                'loan_operations_count': row['loan_operations_count'],
            }
            for rank, row in enumerate(qs, start=1)
        ]
        serializer = BranchLoanActivityReportRowSerializer(rows, many=True)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)
