from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.validators import AppPasswordValidator

__all__ = ['BaseAuthSerializer', 'PASSWORD_FIELD_META']

PASSWORD_FIELD_META = dict(validators=[AppPasswordValidator], write_only=True, required=True,
                           allow_blank=False, trim_whitespace=True)


class BaseAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True, write_only=True, validators=[UniqueValidator])
    password = serializers.CharField(**PASSWORD_FIELD_META)
