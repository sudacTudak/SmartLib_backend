from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser
from .base import BaseAuthSerializer

__all__ = ['RegisterUserSerializer']


class RegisterUserSerializer(BaseAuthSerializer, serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, validators=[
        UniqueValidator(queryset=CustomUser.objects.all(), message='Пользователь с таким email уже существует')])

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'patronymic', 'gender',)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
