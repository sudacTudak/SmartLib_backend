from __future__ import annotations

from rest_framework import serializers

from inventory_movement.enums import InventoryMovementType
from inventory_movement.models import InventoryMovement

__all__ = ['InventoryMovementFundReportSerializer']


class InventoryMovementFundReportSerializer(serializers.ModelSerializer):
    library_branch_address = serializers.CharField(source='library_branch.address', read_only=True)
    staff_full_name = serializers.SerializerMethodField()
    supplier_name = serializers.SerializerMethodField()
    work_title = serializers.CharField(source='work.title', read_only=True)
    movement_summary = serializers.SerializerMethodField()

    class Meta:
        model = InventoryMovement
        fields = (
            'id',
            'library_branch_address',
            'staff_full_name',
            'supplier_name',
            'work_title',
            'type',
            'quantity',
            'reason',
            'movement_summary',
            'created_at',
        )
        read_only_fields = fields

    def get_staff_full_name(self, _movement: InventoryMovement) -> None:
        """В модели движения фонда нет поля сотрудника; зарезервировано под будущие расширения."""
        return None

    def get_supplier_name(self, movement: InventoryMovement) -> str | None:
        if movement.supplier_id is None:
            return None
        return movement.supplier.name

    def get_movement_summary(self, movement: InventoryMovement) -> str:
        title = movement.work.title
        try:
            mtype = InventoryMovementType(movement.type)
        except ValueError:
            return f'{movement.type}: {title}, ×{movement.quantity}'
        if mtype == InventoryMovementType.In:
            return f'Поступление: «{title}», +{movement.quantity}'
        return f'Списание: «{title}», −{movement.quantity}' + (f' ({movement.reason})' if movement.reason else '')
