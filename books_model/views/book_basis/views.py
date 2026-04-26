from django.db.models import Avg, Count, IntegerField, OuterRef, QuerySet, Subquery, Sum
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.permissions import IsAdminUser, SAFE_METHODS

from books_model.models import BookBasis, Book
from common_core.classes import ViewSetBase
from http_core import HTTPResponse

from books_model.serializers import BookBasisSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from django.db import transaction
from typing import cast

from books_model.query_params import BookBasisListQueryParams
from library.models import LibraryBranch

from users.permissions import HasUserPermission, IsStaff
from users.enums import UserPermissions

__all__ = ['BookBasisViewSet']


class BookBasisViewSet(ViewSetBase[QuerySet[BookBasis]], ReadOnlyModelViewSet, CreateModelMixin, UpdateModelMixin,
                       DestroyModelMixin):
    serializer_class = BookBasisSerializer
    queryset = BookBasis.objects.all()

    def get_query_params_model_class(self):
        if self.action == 'list':
            return BookBasisListQueryParams
        return None

    def get_queryset(self) -> QuerySet[BookBasis]:
        qs = super().get_queryset()
        if self.request.method in SAFE_METHODS:
            qs = qs.select_related('genre').prefetch_related('authors').annotate(
                rating_avg=Avg('feedbacks__score'),
                rating_count=Count('feedbacks', distinct=True),
            )
            if self.action in ('list', 'retrieve'):
                books_available_subq = (
                    Book.objects.filter(book_basis_id=OuterRef('pk'))
                    .values('book_basis_id')
                    .annotate(_avail_sum=Sum('available_count'))
                    .values('_avail_sum')[:1]
                )
                qs = qs.annotate(
                    books_available_total=Coalesce(
                        Subquery(books_available_subq, output_field=IntegerField()),
                        0,
                    ),
                )
            if self.action == 'list':
                params = cast(BookBasisListQueryParams | None, self.get_processed_query_params())
                if params is not None and params.only_available is True:
                    qs = qs.filter(books_available_total__gt=0)
        return qs

    def get_permissions(self):
        # TODO: С разработкой нормальной модели пользователя
        # TODO: и добавлением прав поправить на новый permission class
        if self.request.method in SAFE_METHODS:
            return []
        if self.action == 'partial_update':
            return [IsStaff(), HasUserPermission(UserPermissions.BookBasesModification)]
        return [IsStaff(), HasUserPermission(UserPermissions.UsersAdministration)]

    def destroy(self, request, *args, **kwargs):
        book_basis = self.get_object()
        serializer = self.get_serializer(book_basis)
        response_data = serializer.data
        self.perform_destroy(book_basis)
        return HTTPResponse.success(data=response_data, status_code=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer = cast(BookBasisSerializer, serializer)

        with transaction.atomic():
            book_basis = cast(BookBasis, serializer.save())
            library_branches_qs = LibraryBranch.objects.all()

            Book.objects.bulk_create(
                Book(book_basis=book_basis, library_branch=branch, total_count=0, available_count=0) for
                branch in library_branches_qs)
