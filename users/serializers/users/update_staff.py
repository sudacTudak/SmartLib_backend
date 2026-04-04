from rest_framework import serializers

from users.models import CustomUser

__all__ = ['UpdateStaffSerializer']


class UpdateStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'patronymic', 'gender')
