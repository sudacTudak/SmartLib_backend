from rest_framework import serializers

from inventory_movement.models import InventoryMovement

__all__ = ['BaseMovementSerializer']


class BaseMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovement
        fields = ('id', 'type', 'quantity', 'comment', 'created_at')
        read_only_fields = ('id', 'created_at')
