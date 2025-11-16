from django.urls import path

from books_model.views import BookBasisListView, BookBasisDetailView, GenreListView, GenreDetailView

book_bases_url = 'book-bases'
genre_url = 'genre'

urlpatterns = [
    path(fr'{book_bases_url}/', BookBasisListView.as_view(), name='book_basis_list'),
    path(fr'{book_bases_url}/<int:basis_id>', BookBasisDetailView.as_view(), name='book_basis_detail'),
    path(fr'{genre_url}/', GenreListView.as_view(), name='genre_list'),
    path(fr'{genre_url}/<int:genre_id>/', GenreDetailView.as_view(), name='genre_detail')
]
