from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authors.models import Author
from books_model.models import BookBasis

__all__ = ['BookBasisSerializer']


class BookBasisSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        source='author',
        queryset=Author.objects.all(),
        allow_null=True,
        required=False,
    )
    author_name = serializers.CharField(source='author.name', read_only=True)
    rating_avg = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    class Meta:
        model = BookBasis
        fields = (
            'id',
            'title',
            'description',
            'author_id',
            'author_name',
            'publisher',
            'created_year',
            'genre',
            'online_version_link',
            'created_at',
            'updated_at',
            'rating_avg',
            'rating_count',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
            'rating_avg',
            'rating_count',
            'author_name',
        )

    def validate(self, attrs):
        if self.instance is None and not attrs.get('author'):
            raise ValidationError({'author_id': 'Обязательное поле.'})
        return attrs

    @staticmethod
    def get_rating_avg(obj: BookBasis):
        value = getattr(obj, 'rating_avg', None)
        return float(value) if value is not None else None

    @staticmethod
    def get_rating_count(obj: BookBasis) -> int:
        return int(getattr(obj, 'rating_count', 0) or 0)
