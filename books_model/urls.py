from books_model.views import BookBasisViewSet, GenreViewSet
from rest_framework import routers

book_bases_url = 'book-bases'
genre_url = 'genre'

router = routers.SimpleRouter()
router.register(fr'{book_bases_url}', BookBasisViewSet)
router.register(fr'{genre_url}', GenreViewSet)

urlpatterns = router.urls
