from rest_framework import serializers

from works.models import Genre

__all__ = ['GenreSerializer']


class GenreSerializer(serializers.ModelSerializer):
    works = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ['id', 'title', 'created_at', 'updated_at', 'works']
        read_only_fields = ('id', 'created_at', 'updated_at', 'works')

