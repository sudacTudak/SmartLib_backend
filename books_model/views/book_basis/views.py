from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from books_model.models import BookBasis
from http_core import ResponseBodySuccess, ResponseBodyFailure

from books_model.serializers import BookBasisSerializer

__all__ = ['BookBasisListView']


class BookBasisListView(APIView):
    def get(self, request):
        book_bases = BookBasis.objects.all()
        serializer = BookBasisSerializer(book_bases, many=True)
        response_body = ResponseBodySuccess(data=serializer.data, status_code=status.HTTP_200_OK).get_as_dict()
        return Response(response_body)

    def post(self, request):
        serializer = BookBasisSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            saved_book_basis = serializer.save()
            success_response_body = ResponseBodySuccess(data=serializer.validated_data,
                                                        status_code=status.HTTP_201_CREATED).get_as_dict()
            return Response(success_response_body)

        fail_status_code = status.HTTP_400_BAD_REQUEST
        fail_response_body = ResponseBodyFailure(data=serializer.errors,
                                                 status_code=fail_status_code,
                                                 message="Invalid BookBasis data").get_as_dict()
        return Response(fail_response_body, status=fail_status_code)
