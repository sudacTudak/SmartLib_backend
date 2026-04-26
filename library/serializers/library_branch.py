from rest_framework import serializers
from library.models import LibraryBranch
from common_core.drf import AbsoluteMediaUrlMixin, ProcessedImageField

__all__ = ['LibraryBranchSerializer']


class LibraryBranchSerializer(AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    absolute_url_fields = ("preview_link",)
    rating_avg = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    preview_link = ProcessedImageField(required=False, allow_null=True)

    class Meta:
        model = LibraryBranch
        fields = (
            'id',
            'address',
            'preview_link',
            'created_at',
            'updated_at',
            'rating_avg',
            'rating_count',
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'rating_avg', 'rating_count')

    @staticmethod
    def get_rating_avg(obj: LibraryBranch):
        value = getattr(obj, 'rating_avg', None)
        return float(value) if value is not None else None

    @staticmethod
    def get_rating_count(obj: LibraryBranch) -> int:
        return int(getattr(obj, 'rating_count', 0) or 0)

    # validation + minification handled by ProcessedImageField
    # absolute URL conversion handled by AbsoluteMediaUrlMixin
