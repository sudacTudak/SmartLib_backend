from http import HTTPMethod

from typing import cast

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.request import Request

from books_model.models import Book
from books_model.serializers import BookByLibrarySerializer
from common_core.classes import ViewSetBase
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from rest_framework.exceptions import ParseError

from http_core import HTTPResponse
from library.models import LibraryBranch

__all__ = ['BookViewSet']


class BookViewSet(ViewSetBase[Book], RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = BookByLibrarySerializer
    queryset = Book.objects.all()

    def get_permissions(self):
        # TODO: С разработкой нормальной модели пользователя
        # TODO: и добавлением прав поправить на новый permission class
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAdminUser()]

    def get_queryset(self) -> QuerySet[Book]:
        qs = super().get_queryset()

        if self.request.method in SAFE_METHODS:
            qs = qs.select_related('book_basis')

        return qs

    @action(url_path='by-library', detail=False, methods=[HTTPMethod.GET])
    def list_by_library_branch(self, request: Request, *_args, **_kwargs):
        filter_params: dict[str, str | int | bool] = {}

        if (library_branch_id := request.query_params.get('library')) is None:
            raise ParseError(detail='Library branch id is not provided')

        try:
            library_branch_id = int(library_branch_id)
            filter_params['library_branch_id'] = library_branch_id
        except ValueError:
            raise ParseError(detail='Invalid library branch id is provided')

        get_object_or_404(LibraryBranch, pk=library_branch_id)

        if title := request.query_params.get('title'):
            filter_params['title'] = title

        queryset = self.get_queryset().filter(**filter_params)
        serializer = cast(BookByLibrarySerializer, self.get_serializer(queryset, many=True))

        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)
