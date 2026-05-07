from django.db import models
from uuid import uuid4 as uuid

from works.storage_paths import WorkPreviewUploadPath
from works.enums import WorkCategory

__all__ = ['Work', 'WorkFieldsMeta']

WorkFieldsMeta = dict(
    TITLE_MAX_LENGTH=255,
    PUBLISHER_MAX_LENGTH=50,
)


class Work(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid)
    title = models.CharField(max_length=WorkFieldsMeta['TITLE_MAX_LENGTH'])
    description = models.TextField(blank=True, null=True)
    authors = models.ManyToManyField('authors.Author', related_name='works', blank=True)
    category = models.CharField(
        max_length=32,
        choices=WorkCategory.as_django_model_choices(),
    )
    publisher = models.CharField(max_length=WorkFieldsMeta['PUBLISHER_MAX_LENGTH'])
    created_year = models.PositiveIntegerField()
    volume = models.PositiveIntegerField(default=1, verbose_name='Объём (страниц)')
    genres = models.ManyToManyField('works.Genre', related_name='works', blank=True)
    online_version_link = models.TextField(blank=True, null=True)
    preview_link = models.ImageField(upload_to=WorkPreviewUploadPath(), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'work'

    def __str__(self):
        return self.title

