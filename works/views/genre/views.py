from django.db.models import QuerySet
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from rest_framework.viewsets import ReadOnlyModelViewSet

from works.models import Genre
from works.serializers import GenreSerializer
from common_core.classes import ViewSetBase

__all__ = ['GenreViewSet']


class GenreViewSet(
    ViewSetBase[QuerySet[Genre]],
    ReadOnlyModelViewSet,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAdminUser()]

