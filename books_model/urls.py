from books_model.views import BookBasisViewSet, GenreViewSet, BookViewSet
from rest_framework import routers
from http_core import AppRouter, AppRouterConfig

book_bases_url = 'book-bases'
genre_url = 'genre'
book_url = 'book'

router = AppRouter.from_configs((
    AppRouterConfig(prefix=fr'{book_bases_url}', view=BookBasisViewSet),
    AppRouterConfig(prefix=fr'{genre_url}', view=GenreViewSet),
    AppRouterConfig(prefix=fr'{book_url}', view=BookViewSet),
))

# router = routers.SimpleRouter()
# router.register(fr'{book_bases_url}', BookBasisViewSet)
# router.register(fr'{genre_url}', GenreViewSet)
# router.register(fr'{book_url}', BookViewSet)

urlpatterns = router.urls
