from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from books_model.models import BookBasis
from http_core import HTTPResponse

from books_model.serializers import BookBasisSerializer

__all__ = ['BookBasisListView', 'BookBasisDetailView']


class BookBasisListView(APIView):
    def get(self, request: Request):
        book_bases = BookBasis.objects.all()
        serializer = BookBasisSerializer(book_bases, many=True)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = BookBasisSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_201_CREATED)

        return HTTPResponse.failure(data=serializer.errors,
                                    status_code=status.HTTP_400_BAD_REQUEST,
                                    message="Invalid BookBasis data provided")


class BookBasisDetailView(APIView):
    def find_by_id(self, basis_id: int):
        try:
            return BookBasis.objects.get(pk=basis_id)
        except BookBasis.DoesNotExist:
            return None

    def return_not_found(self, basis_id: int):
        return HTTPResponse.failure(status_code=status.HTTP_404_NOT_FOUND,
                                    message=f"Not found Book Basis with id {basis_id}")

    def get(self, _, basis_id: int):
        book_basis = self.find_by_id(basis_id)

        if book_basis is None:
            return self.return_not_found(basis_id)

        serializer = BookBasisSerializer(book_basis)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

    def patch(self, request: Request, basis_id: int):
        book_basis = self.find_by_id(basis_id)

        if book_basis is None:
            return self.return_not_found(basis_id)

        serializer = BookBasisSerializer(data=request.data, instance=book_basis, partial=True)

        if serializer.is_valid():
            serializer.save()
            return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)
        else:
            return HTTPResponse.failure(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST,
                                        message="Invalid BookBasis data provided")

    def delete(self, _: Request, basis_id: int):
        book_basis = self.find_by_id(basis_id)

        if book_basis is None:
            return self.return_not_found(basis_id)

        serializer = BookBasisSerializer(book_basis)
        response_data = serializer.data
        book_basis.delete()

        return HTTPResponse.success(data=response_data, status_code=status.HTTP_200_OK)
