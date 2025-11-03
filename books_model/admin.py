from django.contrib import admin

from .models import BookBasis, Genre

registered_models = (
    BookBasis,
    Genre
)

# Register your models here.
admin.site.register(registered_models)