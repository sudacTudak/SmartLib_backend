from typing import ClassVar

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4 as uuid

from works.models import Work
from inventory_movement.enums import InventoryMovementType
from inventory_movement.manager import InventoryMovementManager
from library.models import LibraryBranch
from suppliers.models import Supplier


class InventoryMovement(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid)
    type = models.CharField(choices=InventoryMovementType.as_django_model_choices(), max_length=3)
    library_branch = models.ForeignKey(LibraryBranch, on_delete=models.PROTECT, related_name='library_branch')
    library_branch_id: str
    work = models.ForeignKey(Work, on_delete=models.PROTECT, related_name='inventory_movements')
    work_id: str
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='supplier', null=True, blank=True)
    supplier_id: str
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    reason = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects: ClassVar[InventoryMovementManager] = InventoryMovementManager()

    class Meta:
        db_table = 'inventory_movements'
        ordering = ('created_at',)

    def clean(self):
        movement_type = InventoryMovementType(self.type)

        if movement_type == InventoryMovementType.In and not self.supplier:
            raise ValidationError('Необходимо указать поставщика для поступления')
        if movement_type == InventoryMovementType.Out and not self.reason:
            raise ValidationError('Необходимо указать причину списания')
