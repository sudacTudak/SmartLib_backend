from rest_framework import serializers

from books_model.models import Genre, BookBasis

__all__ = ['GenreSerializer']


class GenreSerializer(serializers.ModelSerializer):
    book_bases_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ['id', 'title', 'created_at', 'updated_at', 'book_bases_ids']
        read_only_fields = ('id', 'created_at', 'updated_at', 'book_bases_ids')
