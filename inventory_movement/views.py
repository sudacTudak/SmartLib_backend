from __future__ import annotations

from typing import cast

from pydantic import BaseModel, Field
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, ParseError
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from common_core.classes import ViewSetBase
from http_core import HTTPResponse
from inventory_movement.enums import InventoryMovementType
from inventory_movement.models import InventoryMovement
from inventory_movement.queryset import InventoryMovementQuerySet
from users.models import CustomUser
from inventory_movement.serializers.movement_in_write import WriteMovementInSerializer
from inventory_movement.serializers.movement_out_write import WriteMovementOutSerializer
from inventory_movement.serializers.movement_read import ReadInventoryMovementSerializer

__all__ = ['InventoryMovementViewSet', 'InventoryMovementQueryParams']


class InventoryMovementQueryParams(BaseModel):
    type: InventoryMovementType | None = None
    date_from: str | None = Field(None, alias="from")
    date_to: str | None = Field(None, alias="to")

    model_config = {
        "populate_by_name": True
    }


class InventoryMovementViewSet(ViewSetBase[InventoryMovementQuerySet], CreateModelMixin, ListModelMixin):
    queryset = InventoryMovement.objects.all()

    def get_query_params_model_class(self):
        if self.action == 'list':
            return InventoryMovementQueryParams
        return None

    def _get_base_model_queryset(self) -> InventoryMovementQuerySet:
        user = cast(CustomUser, self.request.user)
        return (
            InventoryMovement.objects.select_related('supplier', 'library_branch', 'work')
            .scoped_for_staff_same_library(user)
        )

    def _apply_query_params_for_queryset(self, qs: InventoryMovementQuerySet) -> InventoryMovementQuerySet:
        params = self.get_processed_query_params()
        if params is None:
            return qs

        if params.type:
            qs = qs.filter(type=params.type.value)
        if params.date_from:
            qs = qs.filter(created_at__date__gte=params.date_from)
        if params.date_to:
            qs = qs.filter(created_at__date__lte=params.date_to)

        return qs

    def create(self, request, *args, **kwargs):
        movement_type_raw = request.data.get('type')
        if not movement_type_raw:
            raise ParseError(detail='Поле type обязательно (in | out)')

        try:
            movement_type = InventoryMovementType(movement_type_raw)
        except Exception:
            raise ParseError(detail='Некорректный type. Ожидается: in | out')

        write_serializer_class = (
            WriteMovementInSerializer if movement_type == InventoryMovementType.In else WriteMovementOutSerializer
        )
        serializer = write_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        movement = cast(InventoryMovement, serializer.save())

        read_serializer = ReadInventoryMovementSerializer(movement)
        return HTTPResponse.success(status_code=status.HTTP_201_CREATED, data=read_serializer.data)

    def list(self, request, *args, **kwargs):
        movements = self.filter_queryset(self.get_queryset())
        serializer = ReadInventoryMovementSerializer(movements, many=True)
        return HTTPResponse.success(status_code=status.HTTP_200_OK, data=serializer.data)
