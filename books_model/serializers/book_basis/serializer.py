from rest_framework import serializers

from books_model.models import BookBasis, BookBasisFieldsMeta

__all__ = ['BookBasisSerializer']


class BookBasisSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookBasis
        fields = ('id', 'title', 'description', 'author', 'publisher', 'created_year',
                  'genre', 'online_version_link', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
