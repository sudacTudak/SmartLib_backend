from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books_model.models import BookBasis, Book
from inventory_movement.enums import InventoryMovementType
from inventory_movement.models import InventoryMovement
from inventory_movement.serializers.base import BaseMovementSerializer
from inventory_movement.validators import SingleMovementTypeValidator
from library.models import LibraryBranch

__all__ = ['WriteMovementOutSerializer']


class WriteMovementOutSerializer(BaseMovementSerializer):
    library_branch_id = serializers.PrimaryKeyRelatedField(source='library_branch',
                                                           queryset=LibraryBranch.objects.all())
    book_basis_id = serializers.PrimaryKeyRelatedField(source='book_basis', queryset=BookBasis.objects.all())
    type = serializers.CharField(validators=[SingleMovementTypeValidator(InventoryMovementType.Out)])
    reason = serializers.CharField(allow_blank=False, max_length=255)

    class Meta:
        model = InventoryMovement
        fields = ('library_branch_id', 'book_basis_id', 'type', 'quantity', 'reason', 'comment')

    def create(self, validated_data: dict):
        library_branch = validated_data['library_branch']
        book_basis = validated_data['book_basis']
        quantity = validated_data['quantity']

        with transaction.atomic():
            try:
                book = (
                    Book.objects.select_for_update()
                    .get(library_branch=library_branch, book_basis=book_basis)
                )
            except Book.DoesNotExist:
                raise ValidationError({'book_basis_id': 'Книга не найдена в указанном филиале библиотеки'})

            if book.available_count < quantity:
                raise ValidationError('Недостаточно доступных экземпляров для списания')
            if book.total_count < quantity:
                raise ValidationError('Недостаточно экземпляров на балансе для списания')

            book.total_count -= quantity
            book.available_count -= quantity
            book.save(update_fields=('total_count', 'available_count'))

            return InventoryMovement.objects.create(**validated_data)
