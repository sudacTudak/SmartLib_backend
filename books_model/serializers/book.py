from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, CharField, IntegerField
from books_model.models import Book

__all__ = ['BookByLibrarySerializer']


class BookByLibrarySerializer(ModelSerializer):
    library_branch_id = PrimaryKeyRelatedField(source='library_branch', read_only=True)
    genre_id = PrimaryKeyRelatedField(source='book_basis.genre', read_only=True)

    title = CharField(source='book_basis.title')
    author = CharField(source='book_basis.author')
    publisher = CharField(source='book_basis.publisher')
    description = CharField(source='book_basis.description')
    created_year = IntegerField(source='book_basis.created_year', min_value=1)
    online_version_link = CharField(source='book_basis.online_version_link')

    class Meta:
        model = Book
        fields = ('id', 'library_branch_id', 'genre_id', 'title', 'author', 'publisher', 'description', 'created_year',
                  'online_version_link', 'total_count', 'available_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'title', 'author', 'publisher', 'description', 'created_year', 'online_version_link',
                            'created_at', 'updated_at',)
