from rest_framework import serializers
from rest_framework.fields import CharField

__all__ = ['LogoutSerializer']

class LogoutSerializer(serializers.Serializer):
    refresh = CharField(required=True, allow_blank=False)