from typing import cast

from pydantic import BaseModel, Field, UUID4
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated, AllowAny

from amenity.models import Amenity
from amenity.models.amenity.queryset import AmenityQuerySet
from amenity.serializers import AmenityReadSerializer, AmenityWriteSerializer
from common_core.classes import ViewSetBase
from users.enums import UserRole, UserPermissions
from users.models import CustomUser
from users.permissions import IsStaff, HasUserPermission

__all__ = ['AmenityViewSet', 'AmenityListQueryParams']


class AmenityListQueryParams(BaseModel):
    vendor_id: UUID4 | None = Field(None, alias='vendorId')
    library_branch_id: UUID4 | None = Field(None, alias='libraryBranchId')
    name: str | None = Field(None)

    model_config = {
        'populate_by_name': True,
    }


class AmenityViewSet(
    ViewSetBase[AmenityQuerySet],
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = Amenity.objects.all()

    def get_query_params_model_class(self):
        if self.action == 'list':
            return AmenityListQueryParams
        return None

    def _get_base_model_queryset(self) -> AmenityQuerySet:
        return Amenity.objects.select_related('vendor', 'library_branch')

    def _apply_query_params_for_queryset(self, qs: AmenityQuerySet) -> AmenityQuerySet:
        params = cast(AmenityListQueryParams | None, self.get_processed_query_params())
        if params is None:
            return qs

        if vendor_id := params.vendor_id:
            qs = qs.filter(vendor_id=vendor_id)
        if library_branch_id := params.library_branch_id:
            qs = qs.filter(library_branch_id=library_branch_id)
        if name := params.name:
            qs = qs.filter(vendor__amenity_name__icontains=name)
        return qs

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]

        if self.action in ('create', 'destroy'):
            return [IsStaff(), HasUserPermission(UserPermissions.AmenitiesAdministration)]

        if self.action == 'partial_update':
            return [IsStaff(), HasUserPermission(UserPermissions.AmenitiesModification)]

        return [IsAuthenticated()]

    def get_serializer(self, *args, **kwargs):
        if self.action in ('list', 'retrieve'):
            return AmenityReadSerializer(*args, **kwargs)
        return AmenityWriteSerializer(*args, **kwargs)
