from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from works.models import Work, WorkItem
from inventory_movement.enums import InventoryMovementType
from inventory_movement.models import InventoryMovement
from inventory_movement.serializers.base import BaseMovementSerializer
from inventory_movement.validators import SingleMovementTypeValidator
from library.models import LibraryBranch

__all__ = ['WriteMovementOutSerializer']


class WriteMovementOutSerializer(BaseMovementSerializer):
    library_branch_id = serializers.PrimaryKeyRelatedField(source='library_branch',
                                                           queryset=LibraryBranch.objects.all())
    work_id = serializers.PrimaryKeyRelatedField(source='work', queryset=Work.objects.all())
    type = serializers.CharField(validators=[SingleMovementTypeValidator(InventoryMovementType.Out)])
    reason = serializers.CharField(allow_blank=False, max_length=255)

    class Meta:
        model = InventoryMovement
        fields = ('library_branch_id', 'work_id', 'type', 'quantity', 'reason', 'comment')

    def create(self, validated_data: dict):
        library_branch = validated_data['library_branch']
        work = validated_data['work']
        quantity = validated_data['quantity']

        with transaction.atomic():
            try:
                book = (
                    WorkItem.objects.select_for_update()
                    .get(library_branch=library_branch, work=work)
                )
            except WorkItem.DoesNotExist:
                raise ValidationError({'work_id': 'Экземпляр не найден в указанном филиале библиотеки'})

            if book.available_count < quantity:
                raise ValidationError('Недостаточно доступных экземпляров для списания')
            if book.total_count < quantity:
                raise ValidationError('Недостаточно экземпляров на балансе для списания')

            book.total_count -= quantity
            book.available_count -= quantity
            book.save(update_fields=('total_count', 'available_count'))

            return InventoryMovement.objects.create(**validated_data)
