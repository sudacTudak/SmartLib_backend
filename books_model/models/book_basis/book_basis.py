from django.db import models
from uuid import uuid4 as uuid

from books_model.storage_paths import BookPreviewUploadPath

__all__ = ['BookBasis', 'BookBasisFieldsMeta']

BookBasisFieldsMeta = dict(
    TITLE_MAX_LENGTH=255,
    PUBLISHER_MAX_LENGTH=50,
)

class BookBasis(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid)
    title = models.CharField(max_length=BookBasisFieldsMeta['TITLE_MAX_LENGTH'])
    description = models.TextField(blank=True, null=True)
    authors = models.ManyToManyField('authors.Author', related_name='book_bases', blank=True)
    publisher = models.CharField(max_length=BookBasisFieldsMeta['PUBLISHER_MAX_LENGTH'])
    created_year = models.PositiveIntegerField()
    genre = models.ForeignKey('books_model.Genre', related_name='book_bases_ids', on_delete=models.PROTECT)
    online_version_link = models.TextField(blank=True, null=True)
    preview_link = models.ImageField(upload_to=BookPreviewUploadPath(), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'book_basis'

    def __str__(self):
        return self.title
