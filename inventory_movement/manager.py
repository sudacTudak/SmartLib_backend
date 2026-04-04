from django.db.models.manager import Manager

from inventory_movement.queryset import InventoryMovementQuerySet

__all__ = ['InventoryMovementManager']


class InventoryMovementManager(Manager.from_queryset(InventoryMovementQuerySet)):
    pass
