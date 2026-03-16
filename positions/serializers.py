from rest_framework import serializers

from .constants import POSITION_NAME_MIN_LENGTH
from .models import StaffPosition

__all__ = ['WritePositionSerializer', 'ReadPositionSerializer']


class WritePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPosition
        fields = ('name',)
        extra_kwargs = {'name': {'min_length': POSITION_NAME_MIN_LENGTH, 'write_only': True}}


class ReadPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPosition
        fields = ('id', 'name',)
        read_only_fields = ('id', 'name')
