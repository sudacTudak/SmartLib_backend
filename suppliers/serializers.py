from rest_framework import serializers

from suppliers.models import Supplier

__all__ = ['SupplierSerializer']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id', 'name', 'created_at')
        read_only_fields = ('id', 'created_at')

