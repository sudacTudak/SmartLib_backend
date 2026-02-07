from rest_framework import serializers
from library.models import LibraryBranch

__all__ = ['LibraryBranchSerializer']


class LibraryBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBranch
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
