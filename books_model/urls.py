from books_model.views import BookBasisViewSet, GenreViewSet, BookViewSet
from http_core import AppRouter, AppRouterConfig

book_bases_url = 'book-bases'
genre_url = 'genre'
book_url = 'book'

router = AppRouter.from_configs((
    AppRouterConfig(prefix=fr'{book_bases_url}', view=BookBasisViewSet),
    AppRouterConfig(prefix=fr'{genre_url}', view=GenreViewSet),
    AppRouterConfig(prefix=fr'{book_url}', view=BookViewSet),
))

urlpatterns = router.urls
