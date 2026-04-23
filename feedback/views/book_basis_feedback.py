from http import HTTPMethod

from django.db import IntegrityError
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from books_model.models import BookBasis
from common_core.classes import ViewSetBase
from feedback.models import BookBasisFeedback
from feedback.permissions import IsStaffOrFeedbackOwner
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

    def get_permissions(self):
        if self.action in ('list',):
            return [IsStaff()]

        if self.action in ('by_user', 'create'):
            return [IsAuthenticated()]

        if self.action in ('partial_update', 'destroy'):
            return [IsAuthenticated(), IsStaffOrFeedbackOwner()]

        return [IsAuthenticated()]

    def get_queryset(self) -> QuerySet[BookBasisFeedback]:
        book_basis_id = self.kwargs.get('book_basis_pk')
        return BookBasisFeedback.objects.filter(book_basis_id=book_basis_id).select_related('book_basis', 'client')

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        get_object_or_404(BookBasis, pk=self.kwargs.get('book_basis_pk'))

    def perform_create(self, serializer):
        book_basis = get_object_or_404(BookBasis, pk=self.kwargs.get('book_basis_pk'))
        try:
            serializer.save(book_basis=book_basis, client=self.request.user)
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
