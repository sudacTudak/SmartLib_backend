from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authors.models import Author
from works.enums import WorkCategory
from works.models import Genre
from works.models import Work
from common_core.drf import AbsoluteMediaUrlMixin, ProcessedImageField

__all__ = ['WorkSerializer']


class WorkSerializer(AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    absolute_url_fields = ("preview_link",)
    author_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Author.objects.all(),
        source='authors',
        required=False,
    )
    rating_avg = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    books_available_total = serializers.SerializerMethodField()
    preview_link = ProcessedImageField(required=False, allow_null=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        source="genres",
        queryset=Genre.objects.all(),
        required=False,
    )
    category = serializers.ChoiceField(choices=WorkCategory.as_django_serializer_choices())

    class Meta:
        model = Work
        fields = (
            'id',
            'title',
            'description',
            'author_ids',
            'category',
            'publisher',
            'created_year',
            'volume',
            'genre_ids',
            'online_version_link',
            'preview_link',
            'created_at',
            'updated_at',
            'rating_avg',
            'rating_count',
            'books_available_total',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
            'rating_avg',
            'rating_count',
            'books_available_total',
        )

    def validate(self, attrs):
        if 'authors' in attrs and not attrs['authors']:
            raise ValidationError({'author_ids': 'Список авторов не может быть пустым.'})
        if self.instance is None and not attrs.get('authors'):
            raise ValidationError({'author_ids': 'Укажите хотя бы одного автора.'})
        return attrs

    @staticmethod
    def get_rating_avg(obj: Work):
        value = getattr(obj, 'rating_avg', None)
        return float(value) if value is not None else None

    @staticmethod
    def get_rating_count(obj: Work) -> int:
        return int(getattr(obj, 'rating_count', 0) or 0)

    @staticmethod
    def get_books_available_total(obj: Work) -> int:
        """Сумма `available_count` по всем `WorkItem` с тем же work; без аннотации — 0."""
        v = getattr(obj, 'books_available_total', None)
        return int(v) if v is not None else 0

