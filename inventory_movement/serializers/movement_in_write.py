from django.db import transaction
from rest_framework import serializers

from works.models import Work, WorkItem
from inventory_movement.enums import InventoryMovementType
from inventory_movement.models import InventoryMovement
from inventory_movement.serializers.base import BaseMovementSerializer

from inventory_movement.validators import SingleMovementTypeValidator
from library.models import LibraryBranch
from suppliers.models import Supplier


class WriteMovementInSerializer(BaseMovementSerializer):
    supplier_id = serializers.PrimaryKeyRelatedField(source='supplier', queryset=Supplier.objects.all())
    library_branch_id = serializers.PrimaryKeyRelatedField(source='library_branch',
                                                           queryset=LibraryBranch.objects.all())
    work_id = serializers.PrimaryKeyRelatedField(source='work', queryset=Work.objects.all())
    type = serializers.CharField(validators=[SingleMovementTypeValidator(InventoryMovementType.In)])

    class Meta:
        model = InventoryMovement
        fields = ('supplier_id', 'library_branch_id', 'work_id', 'type', 'quantity', 'comment')

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
                raise serializers.ValidationError(
                    {'work_id': 'Экземпляр не найден в указанном филиале библиотеки'}
                )

            book.total_count += quantity
            book.available_count += quantity
            book.save(update_fields=('total_count', 'available_count'))

            return InventoryMovement.objects.create(**validated_data)
