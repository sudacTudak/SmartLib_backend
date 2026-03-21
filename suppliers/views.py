from rest_framework.mixins import (
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import AllowAny, SAFE_METHODS

from common_core.classes import ViewSetBase
from suppliers.models import Supplier
from suppliers.serializers import SupplierSerializer
from users.enums import UserPermissions
from users.permissions import IsStaff, HasUserPermission

__all__ = ['SupplierViewSet']


class SupplierViewSet(
    ViewSetBase[Supplier],
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsStaff()]

        return [IsStaff(), HasUserPermission(UserPermissions.ManageSuppliers)]
