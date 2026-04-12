from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField

from users.models import CustomUser
from users.serializers.auth.base import PASSWORD_FIELD_META

__all__ = ['ResetPasswordSerializer']


class ResetPasswordSerializer(serializers.Serializer):
    """Сброс пароля без авторизации: email + текущий пароль + новый пароль."""

    email = serializers.EmailField(max_length=254, required=True, write_only=True)
    password = CharField(**PASSWORD_FIELD_META)
    new_password = CharField(**PASSWORD_FIELD_META)
    new_password_repeat = CharField(**PASSWORD_FIELD_META)

    def validate(self, data):
        if data.get('new_password') != data.get('new_password_repeat'):
            raise ValidationError('Новый пароль не соответствует повтору нового пароля')
        return data

    def create(self, validated_data):
        return CustomUser.objects.change_password(
            email=validated_data['email'],
            current_password=validated_data['password'],
            new_password=validated_data['new_password'],
        )
