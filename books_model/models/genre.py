from django.db import models

__all__ = ['Genre']

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.title
