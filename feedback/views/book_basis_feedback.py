from http import HTTPMethod
from typing import cast

from django.db import IntegrityError
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from common_core.classes import ViewSetBase
from feedback.models import BookBasisFeedback
from feedback.permissions import IsStaffOrFeedbackOwner
from feedback.query_params import BookBasisByUserQueryParams
from feedback.serializers import BookBasisFeedbackSerializer
from http_core import HTTPResponse
from users.permissions import IsStaff

__all__ = ['BookBasisFeedbackViewSet']


class BookBasisFeedbackViewSet(
    ViewSetBase[QuerySet[BookBasisFeedback]],
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    serializer_class = BookBasisFeedbackSerializer

    def get_query_params_model_class(self):
        if self.action in ('list', 'by_user'):
            return BookBasisByUserQueryParams
        return None

    def get_permissions(self):
        if self.action in ('list',):
            return [IsStaff()]

        if self.action in ('by_user', 'create'):
            return [IsAuthenticated()]

        if self.action in ('partial_update', 'destroy'):
            return [IsAuthenticated(), IsStaffOrFeedbackOwner()]

        return [IsAuthenticated()]

    def get_queryset(self) -> QuerySet[BookBasisFeedback]:
        if self.action in ('list', 'by_user'):
            params = cast(BookBasisByUserQueryParams | None, self.get_processed_query_params())
            qs = BookBasisFeedback.objects.all().select_related('book_basis', 'client')
            if params is not None and params.book_basis_id is not None:
                qs = qs.filter(book_basis_id=str(params.book_basis_id))
            return qs

        if self.action in ('create', 'partial_update', 'destroy'):
            return BookBasisFeedback.objects.all().select_related('book_basis', 'client')

        return BookBasisFeedback.objects.none()

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError as exc:
            raise ValidationError({'nonFieldErrors': ['Отзыв для этой книги уже существует']}) from exc

    @action(detail=False, methods=[HTTPMethod.GET], url_path='by-user')
    def by_user(self, request: Request, *_args, **_kwargs):
        qs = self.get_queryset()
        if IsStaff().has_permission(request, self):
            client_id = request.query_params.get('client_id') or request.query_params.get('clientId')
            if not client_id:
                return HTTPResponse.failure(
                    message='Укажите client_id',
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            qs = qs.filter(client_id=client_id)
        else:
            qs = qs.filter(client_id=request.user.id)

        serializer = self.get_serializer(qs, many=True)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)
