from __future__ import annotations

import datetime
from http import HTTPMethod
from typing import cast

from pydantic import BaseModel, Field, UUID4
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.request import Request

from work_loan.models import WorkLoan, TypeWorkLoanQuerySet
from work_loan.serializers.work_loan import (
    WorkLoanReadSerializer,
    WorkLoanWriteSerializer,
    WorkLoanProlongSerializer,
)
from common_core.classes import ViewSetBase
from http_core import HTTPResponse
from users.permissions import IsStaff

__all__ = ['WorkLoanViewSet', 'WorkLoanListQueryParams']


class WorkLoanListQueryParams(BaseModel):
    library_branch_id: UUID4 | None = Field(None, alias='libraryBranchId')
    work_item_id: UUID4 | None = Field(None, alias='workItemId')
    client_id: UUID4 | None = Field(None, alias='clientId')
    client_email: str | None = Field(None, alias='clientEmail')
    client_phone: str | None = Field(None, alias='clientPhone')
    loaned_till: datetime.date | None = Field(None, alias='loanedTill')

    date_from: datetime.datetime | None = Field(None, alias='dateFrom')
    date_to: datetime.datetime | None = Field(None, alias='dateTo')

    created_by_id: UUID4 | None = Field(None, alias='createdById')

    model_config = {
        "populate_by_name": True
    }


class WorkLoanViewSet(
    ViewSetBase[QuerySet[WorkLoan]],
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
):
    queryset = WorkLoan.objects.all()

    def get_permissions(self):
        return [IsStaff()]

    def get_query_params_model_class(self):
        if self.action == 'list':
            return WorkLoanListQueryParams
        return None

    def _apply_query_params_for_queryset(self, qs: TypeWorkLoanQuerySet) -> TypeWorkLoanQuerySet:
        params = cast(WorkLoanListQueryParams | None, self.get_processed_query_params())
        if params is None:
            return qs

        if params.library_branch_id:
            qs = qs.filter(library_branch_id=str(params.library_branch_id))
        if params.work_item_id:
            qs = qs.filter(work_item_id=str(params.work_item_id))
        if params.client_id or params.client_email or params.client_phone:
            qs = qs.by_client(client_id=params.client_id, client_email=params.client_email, client_phone=params.client_phone)
        if params.loaned_till:
            qs = qs.filter(loaned_till=params.loaned_till)
        if params.date_from or params.date_to:
            qs = qs.from_to(date_from=params.date_from, date_to=params.date_to)
        if params.created_by_id:
            qs = qs.filter(created_by_id=str(params.created_by_id))

        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return WorkLoanWriteSerializer
        if self.action == 'prolong':
            return WorkLoanProlongSerializer
        return WorkLoanReadSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = cast(WorkLoanWriteSerializer, self.get_serializer(data=request.data))
        serializer.is_valid(raise_exception=True)
        loan = cast(WorkLoan, serializer.save())
        response_serializer = WorkLoanReadSerializer(loan, context=self.get_serializer_context())
        return HTTPResponse.success(data=response_serializer.data, status_code=status.HTTP_201_CREATED)

    @action(url_path='prolong', detail=True, methods=(HTTPMethod.POST,))
    def prolong(self, request: Request, *args, **kwargs):
        loan = cast(WorkLoan, self.get_object())
        serializer = cast(WorkLoanProlongSerializer, self.get_serializer(data=request.data))
        serializer.is_valid(raise_exception=True)

        prolong_time_ms = cast(int, serializer.validated_data['prolong_time'])
        loan = WorkLoan.objects.prolong_work_loan(loan, prolong_for_ms=prolong_time_ms)
        loan.save(update_fields=('loaned_till', 'updated_at'))

        response_serializer = WorkLoanReadSerializer(loan, context=self.get_serializer_context())
        return HTTPResponse.success(data=response_serializer.data, status_code=status.HTTP_200_OK)

