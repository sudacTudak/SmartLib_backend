from rest_framework import serializers

from users.models import CustomUser

__all__ = ['GetUserPublicSerializer']


class GetUserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'patronymic', 'gender', 'is_active', 'created_at',)
        read_only_fields = ('id', 'email', 'first_name', 'last_name', 'patronymic', 'gender', 'is_active', 'created_at',)
