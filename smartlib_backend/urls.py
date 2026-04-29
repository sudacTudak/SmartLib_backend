"""
URL configuration for smartlib_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from .constants import API_PATH_PREFIX

urlpatterns = [
    path(fr'{API_PATH_PREFIX}/django-admin/', admin.site.urls),
    path(fr'{API_PATH_PREFIX}/authors/', include('authors.urls')),
    path(fr'{API_PATH_PREFIX}/works/', include('works.urls')),
    path(fr'{API_PATH_PREFIX}/libs/', include('library.urls')),
    path(fr'{API_PATH_PREFIX}/users/', include('users.urls')),
    path(fr'{API_PATH_PREFIX}/positions/', include('positions.urls')),
    path(fr'{API_PATH_PREFIX}/inventory/', include('inventory_movement.urls')),
    path(fr'{API_PATH_PREFIX}/suppliers/', include('suppliers.urls')),
    path(fr'{API_PATH_PREFIX}/amenities/', include('amenity.urls')),
    path(fr'{API_PATH_PREFIX}/work-loans/', include('work_loan.urls')),
    path(fr'{API_PATH_PREFIX}/feedback/', include('feedback.urls')),
]

# Serve uploaded files via Django (MEDIA) even in production.
# This is OK for early stages; switch to nginx/CDN later for performance.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
