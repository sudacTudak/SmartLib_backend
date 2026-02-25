from django.contrib import admin

from .models import CustomUser, UserPermission

registered_models = (CustomUser, UserPermission,)

admin.site.register(registered_models)
