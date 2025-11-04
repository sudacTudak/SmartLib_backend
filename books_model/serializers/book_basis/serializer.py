from rest_framework import serializers

__all__ = ['BookBasisSerializer']

from books_model.models import BookBasis, BookBasisFieldsMeta


class BookBasisSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(max_length=BookBasisFieldsMeta['TITLE_MAX_LENGTH'])
    # description = serializers.CharField(required=False)
    # author = serializers.CharField(max_length=BookBasisFieldsMeta['AUTHOR_MAX_LENGTH'])
    # publisher = serializers.CharField( max_length=BookBasisFieldsMeta['PUBLISHER_MAX_LENGTH'])
    # created_year = serializers.IntegerField(min_value=0)
    # online_version_link = serializers.URLField(required=False)
    # created_at = serializers.DateTimeField(read_only=True)
    # updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = BookBasis
        fields = ('id', 'title', 'description', 'author', 'publisher', 'created_year',
                  'genre', 'online_version_link', 'created_at', 'updated_at')
