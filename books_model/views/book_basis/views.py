from django.core.serializers import serialize
from django.http import Http404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from books_model.models import BookBasis
from http_core import HTTPResponse

from books_model.serializers import BookBasisSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin

__all__ = ['BookBasisViewSet']


class BookBasisViewSetBase:
    object_name: str | None

    def make_not_found_response(self, field_id: int, **kwargs):
        message = f"Not found {self.object_name} with id {field_id}" \
            if self.object_name is not None else \
            f'Not found object with id {field_id}'
        return HTTPResponse.failure(status_code=status.HTTP_404_NOT_FOUND,
                                    message=message, **kwargs)

    def make_bad_request_response(self, data=None, **kwargs):
        message = f'Invalid {self.object_name} data provided' \
            if self.object_name is not None else \
            'Invalid data provided'
        return HTTPResponse.failure(status_code=status.HTTP_400_BAD_REQUEST, message=message, data=data, **kwargs)

class BookBasisListViewSet(BookBasisViewSetBase, ReadOnlyModelViewSet):
    object_name = BookBasis.__name__
    serializer_class = BookBasisSerializer
    queryset = BookBasis.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            book_basis = self.get_object()
            serializer = self.serializer_class(book_basis)

            return HTTPResponse.success(status_code=status.HTTP_200_OK, data=serializer.data)
        except Http404:
            return self.make_not_found_response(kwargs.get('pk'))


class BookBasisDetailViewSet(BookBasisViewSetBase, GenericViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    object_name = BookBasis.__name__
    serializer_class = BookBasisSerializer
    queryset = BookBasis.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if (serializer.is_valid()):
            self.perform_create(serializer)
            return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_201_CREATED)
        else:
            return self.make_bad_request_response(serializer.errors)

    def partial_update(self, request, *args, **kwargs):
        try:
            book_basis = self.get_object()
            serializer = self.get_serializer(book_basis, data=request.data, partial=True)

            if (serializer.is_valid()):
                self.perform_update(serializer)
                return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)
            else:
                return self.make_bad_request_response(serializer.errors)
        except Http404:
            return self.make_not_found_response(kwargs.get('pk'))

    def destroy(self, request, *args, **kwargs):
        try:
            book_basis = self.get_object()
            serializer = self.get_serializer(book_basis)
            response_data = serializer.data
            self.perform_destroy(book_basis)
            return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

        except Http404:
            return self.make_not_found_response(kwargs.get('pk'))

class BookBasisViewSet(BookBasisListViewSet, BookBasisDetailViewSet):
    pass

# class BookBasisListView(APIView):
#     def get(self, request: Request):
#         book_bases = BookBasis.objects.all()
#         serializer = BookBasisSerializer(book_bases, many=True)
#         return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)
#
#     def post(self, request: Request):
#         serializer = BookBasisSerializer(data=request.data)
#
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_201_CREATED)
#
#         return HTTPResponse.failure(data=serializer.errors,
#                                     status_code=status.HTTP_400_BAD_REQUEST,
#                                     message="Invalid BookBasis data provided")
#
#
# class BookBasisDetailView(APIView):
#     def find_by_id(self, basis_id: int):
#         try:
#             return BookBasis.objects.get(pk=basis_id)
#         except BookBasis.DoesNotExist:
#             return None
#
#     def return_not_found(self, basis_id: int):
#         return HTTPResponse.failure(status_code=status.HTTP_404_NOT_FOUND,
#                                     message=f"Not found Book Basis with id {basis_id}")
#
#     def get(self, _, basis_id: int):
#         book_basis = self.find_by_id(basis_id)
#
#         if book_basis is None:
#             return self.return_not_found(basis_id)
#
#         serializer = BookBasisSerializer(book_basis)
#         return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)
#
#     def patch(self, request: Request, basis_id: int):
#         book_basis = self.find_by_id(basis_id)
#
#         if book_basis is None:
#             return self.return_not_found(basis_id)
#
#         serializer = BookBasisSerializer(data=request.data, instance=book_basis, partial=True)
#
#         if serializer.is_valid():
#             serializer.save()
#             return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)
#         else:
#             return HTTPResponse.failure(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST,
#                                         message="Invalid BookBasis data provided")
#
#     def delete(self, _: Request, basis_id: int):
#         book_basis = self.find_by_id(basis_id)
#
#         if book_basis is None:
#             return self.return_not_found(basis_id)
#
#         serializer = BookBasisSerializer(book_basis)
#         response_data = serializer.data
#         book_basis.delete()
#
#         return HTTPResponse.success(data=response_data, status_code=status.HTTP_200_OK)
