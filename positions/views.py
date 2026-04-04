from django.db.models import QuerySet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin

from common_core.classes import ViewSetBase
from positions.models import StaffPosition
from positions.serializers import WritePositionSerializer, ReadPositionSerializer
from users.permissions import IsStaff, HasUserPermission
from users.enums import UserPermissions

__all__ = ['PositionsViewSet']


class PositionsViewSet(ViewSetBase[QuerySet[StaffPosition]], ListModelMixin, UpdateModelMixin, CreateModelMixin,
                       DestroyModelMixin):
    queryset = StaffPosition.objects.all()
    serializer_class = WritePositionSerializer

    def get_permissions(self):
        if self.action in ('partial_update',):
            return IsStaff(), HasUserPermission(UserPermissions.PositionsModification),

        if self.action in ('create', 'destroy',):
            return IsStaff(), HasUserPermission(UserPermissions.PositionsAdministration)

        return (IsStaff(),)

    def get_serializer(self, *args, **kwargs):
        if self.action in ('list', 'retrieve',):
            return ReadPositionSerializer(*args, **kwargs)

        return WritePositionSerializer(*args, **kwargs)
