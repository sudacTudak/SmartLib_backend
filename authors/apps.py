from django.apps import AppConfig

__all__ = ['AuthorsConfig']


class AuthorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authors'
