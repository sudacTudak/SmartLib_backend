from http_core import AppRouter
from book_loan.views import BookLoanViewSet

router = AppRouter.from_configs((
    AppRouter.Config(view=BookLoanViewSet, basename='book-loan'),
))

urlpatterns = router.urls

