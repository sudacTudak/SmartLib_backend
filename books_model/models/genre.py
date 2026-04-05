from django.db import models
from uuid import uuid4 as uuid

__all__ = ['Genre']


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'genre'

    def __str__(self):
        return self.title
