from django.apps import AppConfig

__all__ = ['WorkLoanConfig']


class WorkLoanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'work_loan'
    label = 'book_loan'

