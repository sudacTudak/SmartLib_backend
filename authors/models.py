from uuid import uuid4

from django.db import models

__all__ = ['Author']


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'author'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name
