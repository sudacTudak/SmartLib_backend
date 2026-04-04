from common_core.classes import ViewSetBase
from users.models import CustomUser, CustomUserQuerySet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from users.serializers import GetUserPublicSerializer

__all__ = ['UsersViewSet']

class UsersViewSet(ViewSetBase[CustomUserQuerySet], RetrieveModelMixin, ListModelMixin):
    queryset = CustomUser.objects.all()

    def get_queryset(self) -> CustomUserQuerySet:
        return CustomUser.objects.get_clients()

    def get_serializer(self, *args, **kwargs):
        return GetUserPublicSerializer(*args, **kwargs)


