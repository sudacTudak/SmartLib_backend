from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from users.models import CustomUser
from users.serializers.auth.base import PASSWORD_FIELD_META, BaseAuthSerializer

__all__ = ['ChangePasswordSerializer']


class ChangePasswordSerializer(BaseAuthSerializer):
    new_password = CharField(**PASSWORD_FIELD_META)
    new_password_repeat = CharField(**PASSWORD_FIELD_META)

    def validate(self, data):
        new_password: str = data.get('new_password')
        new_password_repeat: str = data.get('new_password_repeat')

        if new_password != new_password_repeat:
            raise ValidationError('Новый пароль не соответствует повтору нового пароля')

        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return CustomUser.objects.change_password(email=validated_data.get('email'),
                                                  current_password=validated_data.get('password'),
                                                  new_password=validated_data.get('new_password'))
