from django.db.models import QuerySet

from common_core.classes import ViewSetBase
from users.models import CustomUser, CustomUserQuerySet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin

from users.serializers import CreateUserSerializer, GetUserPublicSerializer

__all__ = ['UsersViewSet']

class UsersViewSet(ViewSetBase[CustomUser], CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    queryset = CustomUser.objects.all()

    def get_queryset(self) -> CustomUserQuerySet:
        return CustomUser.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action in ('create', 'partial_update',):
            return CreateUserSerializer

        return GetUserPublicSerializer


