from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet

from books_model.models import Genre
from books_model.serializers import GenreSerializer
from common_core.classes import ViewSetBase

__all__ = ['GenreListViewSet', 'GenreDetailViewSet', 'GenreViewSet']


class GenreListViewSet(ViewSetBase, ReadOnlyModelViewSet):
    object_name = Genre.__name__
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetailViewSet(ViewSetBase, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    object_name = Genre.__name__
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreViewSet(GenreListViewSet, GenreDetailViewSet):
    pass
