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

from book_loan.models import BookLoan, TypeBookLoanQuerySet
from book_loan.serializers.book_loan import (
    BookLoanReadSerializer,
    BookLoanWriteSerializer,
    BookLoanProlongSerializer,
)
from common_core.classes import ViewSetBase
from http_core import HTTPResponse
from users.permissions import IsStaff

__all__ = ['BookLoanViewSet', 'BookLoanListQueryParams']


class BookLoanListQueryParams(BaseModel):
    library_branch_id: UUID4 | None = Field(None, alias='libraryBranchId')
    book_id: UUID4 | None = Field(None, alias='bookId')
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


class BookLoanViewSet(
    ViewSetBase[QuerySet[BookLoan]],
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
):
    queryset = BookLoan.objects.all()

    def get_permissions(self):
        return [IsStaff()]

    def get_query_params_model_class(self):
        if self.action == 'list':
            return BookLoanListQueryParams
        return None

    def _apply_query_params_for_queryset(self, qs: TypeBookLoanQuerySet) -> TypeBookLoanQuerySet:
        params = cast(BookLoanListQueryParams | None, self.get_processed_query_params())
        if params is None:
            return qs

        if params.library_branch_id:
            qs = qs.filter(library_branch_id=str(params.library_branch_id))
        if params.book_id:
            qs = qs.filter(book_id=str(params.book_id))
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
            return BookLoanWriteSerializer
        if self.action == 'prolong':
            return BookLoanProlongSerializer
        return BookLoanReadSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = cast(BookLoanWriteSerializer, self.get_serializer(data=request.data))
        serializer.is_valid(raise_exception=True)
        loan = cast(BookLoan, serializer.save())
        response_serializer = BookLoanReadSerializer(loan, context=self.get_serializer_context())
        return HTTPResponse.success(data=response_serializer.data, status_code=status.HTTP_201_CREATED)

    @action(url_path='prolong', detail=True, methods=(HTTPMethod.POST,))
    def prolong(self, request: Request, *args, **kwargs):
        loan = cast(BookLoan, self.get_object())
        serializer = cast(BookLoanProlongSerializer, self.get_serializer(data=request.data))
        serializer.is_valid(raise_exception=True)

        prolong_time_ms = cast(int, serializer.validated_data['prolong_time'])
        loan = BookLoan.objects.prolong_book_loan(loan, prolong_for_ms=prolong_time_ms)
        loan.save(update_fields=('loaned_till', 'updated_at'))

        response_serializer = BookLoanReadSerializer(loan, context=self.get_serializer_context())
        return HTTPResponse.success(data=response_serializer.data, status_code=status.HTTP_200_OK)

