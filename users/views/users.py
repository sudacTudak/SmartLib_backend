from common_core.classes import ViewSetBase
from users.models import CustomUser, CustomUserQuerySet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin

from users.serializers import CreateStaffSerializer, GetUserPublicSerializer

__all__ = ['UsersViewSet']

class UsersViewSet(ViewSetBase[CustomUser], RetrieveModelMixin, ListModelMixin):
    queryset = CustomUser.objects.all()

    def get_queryset(self) -> CustomUserQuerySet:
        return CustomUser.objects.get_clients()

    def get_serializer(self, *args, **kwargs):
        if self.action in ('create', 'partial_update',):
            return CreateStaffSerializer(*args, **kwargs)

        return GetUserPublicSerializer(*args, **kwargs)


