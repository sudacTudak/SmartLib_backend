from django.urls import path, include

from books_model.views import BookBasisViewSet, GenreListView, GenreDetailView
from rest_framework import routers

book_bases_url = 'book-bases'
genre_url = 'genre'

router = routers.SimpleRouter()
router.register(fr'{book_bases_url}', BookBasisViewSet)

urlpatterns = [
    # path(fr'{book_bases_url}/', BookBasisListView.as_view(), name='book_basis_list'),
    # path(fr'{book_bases_url}/<int:basis_id>', BookBasisDetailView.as_view(), name='book_basis_detail'),
    path('', include(router.urls)),
    path(fr'{genre_url}/', GenreListView.as_view(), name='genre_list'),
    path(fr'{genre_url}/<int:genre_id>/', GenreDetailView.as_view(), name='genre_detail')
]
