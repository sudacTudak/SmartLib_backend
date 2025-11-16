__all__ = ['GenreListView', 'GenreDetailView']

from rest_framework.request import Request
from rest_framework.views import APIView
from books_model.models import Genre
from books_model.serializers import GenreSerializer
from http_core import HTTPResponse
from rest_framework import status


class GenreListView(APIView):
    def get(self, _: Request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = GenreSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return HTTPResponse.success(data=serializer.validated_data, status_code=status.HTTP_201_CREATED)
        else:
            return HTTPResponse.failure(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST,
                                        message='Invalid Genre data provided')


class GenreDetailView(APIView):
    def get_by_id(self, genre_id: int):
        try:
            return Genre.objects.get(pk=genre_id)
        except Genre.DoesNotExist:
            return None


    def return_not_found(self, genre_id: int):
        return HTTPResponse.failure(status_code=status.HTTP_404_NOT_FOUND,
                                    message=f'Genre with id: {genre_id} not found')

    def get(self, _, genre_id: int):
        genre = self.get_by_id(genre_id)

        if genre is None:
            return self.return_not_found(genre_id)

        serializer = GenreSerializer(genre)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

    def patch(self, request: Request, genre_id: int):
        genre = self.get_by_id(genre_id)

        if genre is None:
            return self.return_not_found(genre_id)

        serializer = GenreSerializer(data=request.data, instance=genre, partial=True)

        if serializer.is_valid():
            serializer.save()
            return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)
        else:
            return HTTPResponse.failure(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST,
                                        message='Invalid Genre data provided')

    def delete(self, request: Request, genre_id: int):
        genre = self.get_by_id(genre_id)

        if genre is None:
            return self.return_not_found(genre_id)

        serializer = GenreSerializer(genre)
        response_data = serializer.data
        genre.delete()

        return HTTPResponse.success(data=response_data, status_code=status.HTTP_200_OK)
