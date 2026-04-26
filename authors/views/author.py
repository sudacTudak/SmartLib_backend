from django.db.models import QuerySet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import SAFE_METHODS
from authors.models import Author
from authors.serializers import AuthorSerializer
from common_core.classes import ViewSetBase
from users.permissions import IsStaff

__all__ = ['AuthorViewSet']


class AuthorViewSet(
    ViewSetBase[QuerySet[Author]],
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [IsStaff()]
