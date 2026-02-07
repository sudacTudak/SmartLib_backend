from django.contrib import admin

from .models import BookBasis, Genre, Book

registered_models = (
    BookBasis,
    Book,
    Genre
)

# Register your models here.
admin.site.register(registered_models)