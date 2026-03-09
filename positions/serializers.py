from rest_framework import serializers
from .models import Position

__all__ = ['PositionSerializer']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = 'name'