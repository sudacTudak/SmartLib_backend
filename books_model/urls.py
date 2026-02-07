from books_model.views import BookBasisViewSet, GenreViewSet, BookViewSet
from rest_framework import routers

book_bases_url = 'book-bases'
genre_url = 'genre'
book_url = 'book'

router = routers.SimpleRouter()
router.register(fr'{book_bases_url}', BookBasisViewSet)
router.register(fr'{genre_url}', GenreViewSet)
router.register(fr'{book_url}', BookViewSet)

urlpatterns = router.urls
