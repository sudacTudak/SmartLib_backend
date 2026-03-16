from books_model.views import BookBasisViewSet, GenreViewSet, BookViewSet
from http_core import AppRouter

book_bases_url = 'book-bases'
genre_url = 'genre'
book_url = 'book'

router = AppRouter.from_configs((
    AppRouter.Config(prefix=fr'{book_bases_url}', view=BookBasisViewSet),
    AppRouter.Config(prefix=fr'{genre_url}', view=GenreViewSet),
    AppRouter.Config(prefix=fr'{book_url}', view=BookViewSet),
))

urlpatterns = router.urls
