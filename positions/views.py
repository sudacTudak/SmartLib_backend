from django.views.generic import ListView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin

from common_core.classes import ViewSetBase
from positions.models import Position
from positions.serializers import PositionSerializer
from users.permissions import IsStaff, HasUserPermission
from users.enums import UserPermissions

__all__ = ['PositionsViewSet']


class PositionsViewSet(ViewSetBase[Position], ListModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def get_permissions(self):
        if self.action in ('partial_update',):
            return IsStaff(), HasUserPermission(UserPermissions.PositionsModification),

        if self.action in ('create', 'destroy',):
            return IsStaff(), HasUserPermission(UserPermissions.PositionsAdministration)

        return (IsStaff(),)
