from rest_framework.exceptions import ValidationError

from inventory_movement.enums import InventoryMovementType

__all__ = ['SingleMovementTypeValidator']


class SingleMovementTypeValidator:
    expected_type: InventoryMovementType

    def __init__(self, expected_type: InventoryMovementType, /):
        self.expected_type = expected_type

    def __call__(self, value):
        movement_type = InventoryMovementType(value)

        if movement_type != self.expected_type:
            raise ValidationError(
                f'Тип движения не соответствует ожидаемому: ожидался {self.expected_type}, получено {movement_type}')
