from rest_framework import serializers
from users.models import UserPermission

__all__ = ['ReadUserPermissionsSerializer']

class ReadUserPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = ('id', 'code',)
        read_only_fields = ('id', 'code',)