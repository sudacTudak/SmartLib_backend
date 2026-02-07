from django.contrib import admin

from library.models import LibraryBranch

registered_models = (
    LibraryBranch
)

admin.site.register(registered_models)
