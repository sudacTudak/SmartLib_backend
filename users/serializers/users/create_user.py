from rest_framework import serializers

from users.models import CustomUser
from users.validators import AppPasswordValidator

__all__ = ['CreateUserSerializer']


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=6, write_only=True, required=True,
                                     validators=[AppPasswordValidator])

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'patronymic', 'gender', 'role')
