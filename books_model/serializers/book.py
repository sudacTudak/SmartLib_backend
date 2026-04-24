from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import CharField, IntegerField, ModelSerializer, UUIDField
from books_model.models import Book

__all__ = ['BookByLibrarySerializer']


class BookByLibrarySerializer(ModelSerializer):
    library_branch_id = PrimaryKeyRelatedField(source='library_branch', read_only=True)
    genre_id = PrimaryKeyRelatedField(source='book_basis.genre', read_only=True)
    author_id = UUIDField(source='book_basis.author_id', read_only=True)
    author_name = CharField(source='book_basis.author.name', read_only=True)

    title = CharField(source='book_basis.title')
    publisher = CharField(source='book_basis.publisher')
    description = CharField(source='book_basis.description')
    created_year = IntegerField(source='book_basis.created_year', min_value=1)
    online_version_link = CharField(source='book_basis.online_version_link')

    class Meta:
        model = Book
        fields = (
            'id',
            'library_branch_id',
            'genre_id',
            'title',
            'author_id',
            'author_name',
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
            'title',
            'author_id',
            'author_name',
            'publisher',
            'description',
            'created_year',
            'online_version_link',
            'created_at',
            'updated_at',
        )
