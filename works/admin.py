from django.contrib import admin

from .models import Work, Genre, WorkItem

registered_models = (
    Work,
    WorkItem,
    Genre
)

admin.site.register(registered_models)

