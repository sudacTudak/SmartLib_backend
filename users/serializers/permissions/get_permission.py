from rest_framework import serializers

from users.models import UserPermission

__all__ = ['GetPermissionSerializer']

class GetPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        # fields = ('id', 'code', 'created_at', 'updated_at', 'users')
        fields = '__all__'