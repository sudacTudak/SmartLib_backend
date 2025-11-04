from django.urls import path

from books_model.views import BookBasisListView
from smartlib_backend.constants import API_PATH_PREFIX

urlpatterns = [
    path(r'/', BookBasisListView.as_view(), name='book_basis_list'),
]
