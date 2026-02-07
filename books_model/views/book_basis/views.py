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

__all__ = ['BookBasisViewSet']

from library.models import LibraryBranch


class BookBasisViewSet(ViewSetBase[BookBasis], ReadOnlyModelViewSet, CreateModelMixin, UpdateModelMixin,
                       DestroyModelMixin):
    serializer_class = BookBasisSerializer
    queryset = BookBasis.objects.all()

    def get_permissions(self):
        # TODO: С разработкой нормальной модели пользователя
        # TODO: и добавлением прав поправить на новый permission class
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAdminUser()]

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
