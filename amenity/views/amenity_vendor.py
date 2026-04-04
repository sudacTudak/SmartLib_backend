from django.db.models import QuerySet
from pydantic import BaseModel, Field
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, \
    RetrieveModelMixin

from amenity.models import AmenityVendor
from amenity.serializers import AmenityVendorReadSerializer, AmenityVendorWriteSerializer
from common_core.classes import ViewSetBase
from users.permissions import IsStaff, HasUserPermission
from users.enums import UserPermissions
from typing import cast


class AmenityVendorQueryParams(BaseModel):
    vendor_name: str | None = Field(None, alias='vendorName')
    amenity_name: str | None = Field(None, alias='amenityName')

    model_config = {
        'populate_by_name': True,
    }


class AmenityVendorViewSet(ViewSetBase[QuerySet[AmenityVendor]],
                           AmenityVendor, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
                           DestroyModelMixin):

    queryset = AmenityVendor.objects.all()

    def get_permissions(self):
        if self.action in ('list', 'retrieve',):
            return [IsStaff(),]
        if self.action == 'partial_update':
            return [IsStaff(), HasUserPermission(UserPermissions.AmenityVendorModification),]
        if self.action in ('create', 'destroy'):
            return [IsStaff(), HasUserPermission(UserPermissions.AmenityVendorAdministration),]

        return [IsStaff(), HasUserPermission(UserPermissions.AmenityVendorAdministration),]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return AmenityVendorReadSerializer

        if self.action in ('create', 'partial_update',):
            return AmenityVendorWriteSerializer

        return AmenityVendorReadSerializer

    def _apply_query_params_for_queryset(self, qs: QuerySet[AmenityVendor]) -> QuerySet[AmenityVendor]:
        if (query_params := cast(AmenityVendorQueryParams | None, self.get_processed_query_params())) is None:
            return qs

        if vendor_name := query_params.vendor_name:
            qs.filter(vendor_name=vendor_name)
        if amenity_name := query_params.amenity_name:
            qs.filter(amenity_name=amenity_name)

        return qs

