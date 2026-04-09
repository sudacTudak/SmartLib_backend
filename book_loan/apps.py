from django.apps import AppConfig

__all__ = ['BookLoanConfig']


class BookLoanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book_loan'
