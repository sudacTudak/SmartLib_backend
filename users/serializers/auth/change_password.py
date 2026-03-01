from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField
from rest_framework import serializers

from users.models import CustomUser
from users.validators import password_validator

password_field_meta = dict(min_length=6, max_length=30, validators=[password_validator], write_only=True, required=True,
                           allow_blank=False, trim_whitespace=True)

__all__ = ['ChangePasswordSerializer']

class ChangePasswordSerializer(serializers.Serializer):
    email = EmailField(required=True, write_only=True)
    current_password = CharField(**password_field_meta)
    new_password = CharField(**password_field_meta)
    new_password_repeat = CharField(**password_field_meta)

    def validate(self, data):
        new_password: str = data['new_password']
        new_password_repeat: str = data['new_password_repeat']

        if new_password != new_password_repeat:
            raise ValidationError('Новый пароль не соответствует повтору нового пароля')

        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return CustomUser.objects.change_password(email=validated_data['email'],
                                                  current_password=validated_data['current_password'],
                                                  new_password=validated_data['new_password'])
