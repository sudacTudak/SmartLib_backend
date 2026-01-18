from django.core.serializers import serialize
from django.http import Http404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from books_model.models import BookBasis
from common_core.classes import ViewSetBase
from http_core import HTTPResponse

from books_model.serializers import BookBasisSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin

__all__ = ['BookBasisViewSet']


class BookBasisListViewSet(ViewSetBase, ReadOnlyModelViewSet):
    object_name = BookBasis.__name__
    serializer_class = BookBasisSerializer
    queryset = BookBasis.objects.all()


class BookBasisDetailViewSet(ViewSetBase, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    object_name = BookBasis.__name__
    serializer_class = BookBasisSerializer
    queryset = BookBasis.objects.all()

    def destroy(self, request, *args, **kwargs):
        book_basis = self.get_object()
        serializer = self.get_serializer(book_basis)
        response_data = serializer.data
        self.perform_destroy(book_basis)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)


class BookBasisViewSet(BookBasisListViewSet, BookBasisDetailViewSet):
    pass
