from pydantic import BaseModel, Field, ValidationError
from rest_framework.exceptions import ParseError
from rest_framework.mixins import (
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import SAFE_METHODS

from common_core.classes import ViewSetBase
from suppliers.models import Supplier
from suppliers.serializers import SupplierSerializer
from users.enums import UserPermissions
from users.permissions import IsStaff, HasUserPermission

__all__ = ['SupplierViewSet', 'SupplierListQueryParams']


class SupplierListQueryParams(BaseModel):
    name: str | None = Field(None)

    model_config = {
        'populate_by_name': True,
    }


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

    def get_queryset(self):
        qs = super().get_queryset()

        try:
            params = SupplierListQueryParams.model_validate(self.get_raw_query_params())
        except ValidationError as exc:
            raise ParseError(detail=exc.errors())

        if name := params.name:
            qs = qs.filter(name__icontains=name)

        return qs

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsStaff()]

        return [IsStaff(), HasUserPermission(UserPermissions.ManageSuppliers)]
