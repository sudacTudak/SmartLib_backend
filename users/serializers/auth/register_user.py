from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser

__all__ = ['RegisterUserSerializer']

from users.validators import password_validator


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=30, validators=[password_validator])
    email = serializers.EmailField(max_length=254, validators=[
        UniqueValidator(queryset=CustomUser.objects.all(), message='Пользователь с таким email уже существует')])

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'patronymic', 'gender')

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
