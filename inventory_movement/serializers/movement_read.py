from rest_framework import serializers

from inventory_movement.models import InventoryMovement
from inventory_movement.serializers.base import BaseMovementSerializer

__all__ = ['ReadInventoryMovementSerializer']


class ReadInventoryMovementSerializer(BaseMovementSerializer):
    supplier_id = serializers.UUIDField(source='supplier_id', allow_null=True)
    library_branch_id = serializers.UUIDField(source='library_branch_id')
    work_id = serializers.UUIDField(source='work_id')

    class Meta:
        model = InventoryMovement
        fields = (
            'id',
            'type',
            'library_branch_id',
            'work_id',
            'supplier_id',
            'quantity',
            'reason',
            'comment',
            'created_at',
        )
        read_only_fields = ('id', 'created_at')
