from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import CharField, IntegerField, ModelSerializer
from works.models import WorkItem

__all__ = ['WorkItemByLibrarySerializer']


class WorkItemByLibrarySerializer(ModelSerializer):
    library_branch_id = PrimaryKeyRelatedField(source='library_branch', read_only=True)
    work_id = PrimaryKeyRelatedField(source='work', read_only=True)
    category = serializers.CharField(source='work.category', read_only=True)
    genre_ids = serializers.SerializerMethodField()
    author_ids = serializers.SerializerMethodField()

    title = CharField(source='work.title')
    publisher = CharField(source='work.publisher')
    description = CharField(source='work.description')
    created_year = IntegerField(source='work.created_year', min_value=1)
    online_version_link = CharField(source='work.online_version_link')

    class Meta:
        model = WorkItem
        fields = (
            'id',
            'library_branch_id',
            'work_id',
            'category',
            'genre_ids',
            'title',
            'author_ids',
            'publisher',
            'description',
            'created_year',
            'online_version_link',
            'total_count',
            'available_count',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'work_id',
            'category',
            'title',
            'genre_ids',
            'author_ids',
            'publisher',
            'description',
            'created_year',
            'online_version_link',
            'created_at',
            'updated_at',
        )

    @staticmethod
    def get_author_ids(obj: WorkItem) -> list[str]:
        return [str(aid) for aid in obj.work.authors.order_by('name').values_list('id', flat=True)]

    @staticmethod
    def get_genre_ids(obj: WorkItem) -> list[str]:
        return [str(gid) for gid in obj.work.genres.order_by('title').values_list('id', flat=True)]

