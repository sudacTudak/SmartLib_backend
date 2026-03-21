from __future__ import annotations

from typing import cast

from pydantic import BaseModel, Field, ValidationError
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from common_core.classes import ViewSetBase
from http_core import HTTPResponse
from inventory_movement.enums import InventoryMovementType
from inventory_movement.models import InventoryMovement
from inventory_movement.serializers.movement_in_write import WriteMovementInSerializer
from inventory_movement.serializers.movement_out_write import WriteMovementOutSerializer
from inventory_movement.serializers.movement_read import ReadInventoryMovementSerializer

__all__ = ['InventoryMovementViewSet']


class InventoryMovementQueryParams(BaseModel):
    type: InventoryMovementType | None = None
    date_from: str | None = Field(None, alias="from")
    date_to: str | None = Field(None, alias="to")

    model_config = {
        "populate_by_name": True
    }


class InventoryMovementViewSet(ViewSetBase[InventoryMovement], CreateModelMixin, ListModelMixin):
    queryset = InventoryMovement.objects.all()

    def get_queryset(self):
        qs = super().get_queryset().select_related('supplier', 'library_branch', 'book_basis')

        try:
            params = InventoryMovementQueryParams.model_validate(self.get_raw_query_params())
        except ValidationError as exc:
            raise ParseError(detail=exc.errors())

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
