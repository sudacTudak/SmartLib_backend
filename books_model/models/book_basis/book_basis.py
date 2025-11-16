from django.db import models

__all__ = ['BookBasis', 'BookBasisFieldsMeta']

BookBasisFieldsMeta = dict(
    TITLE_MAX_LENGTH = 255,
    AUTHOR_MAX_LENGTH = 50,
    PUBLISHER_MAX_LENGTH = 50
)

class BookBasis(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=BookBasisFieldsMeta['TITLE_MAX_LENGTH'])
    description = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=BookBasisFieldsMeta['AUTHOR_MAX_LENGTH'])
    publisher = models.CharField(max_length=BookBasisFieldsMeta['PUBLISHER_MAX_LENGTH'])
    created_year = models.PositiveIntegerField()
    genre = models.ForeignKey('books_model.Genre', related_name='book_bases_ids', on_delete=models.PROTECT)
    online_version_link = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'book_basis'

    def __str__(self):
        return self.title
