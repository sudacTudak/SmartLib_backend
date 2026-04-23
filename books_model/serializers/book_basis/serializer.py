from rest_framework import serializers

from books_model.models import BookBasis, BookBasisFieldsMeta

__all__ = ['BookBasisSerializer']


class BookBasisSerializer(serializers.ModelSerializer):
    rating_avg = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    class Meta:
        model = BookBasis
        fields = (
            'id',
            'title',
            'description',
            'author',
            'publisher',
            'created_year',
            'genre',
            'online_version_link',
            'created_at',
            'updated_at',
            'rating_avg',
            'rating_count',
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'rating_avg', 'rating_count')

    @staticmethod
    def get_rating_avg(obj: BookBasis):
        value = getattr(obj, 'rating_avg', None)
        return float(value) if value is not None else None

    @staticmethod
    def get_rating_count(obj: BookBasis) -> int:
        return int(getattr(obj, 'rating_count', 0) or 0)
