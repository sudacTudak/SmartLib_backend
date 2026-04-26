from rest_framework import serializers

from authors.models import Author

__all__ = ['AuthorSerializer']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name')
        read_only_fields = ('id',)
