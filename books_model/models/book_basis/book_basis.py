from django.db import models

__all__ = ['BookBasis']

class BookBasis(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    created_year = models.PositiveIntegerField()
    genre = models.ForeignKey('books_model.Genre', on_delete=models.PROTECT)
    online_version_link = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.title