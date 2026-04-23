from http_core import AppRouter

from feedback.views import BookBasisFeedbackViewSet, LibraryBranchFeedbackViewSet

router = AppRouter.from_configs(
    (
        AppRouter.Config(
            prefix=r'books/book-bases/(?P<book_basis_pk>[^/.]+)/feedbacks',
            view=BookBasisFeedbackViewSet,
            basename='book-basis-feedback',
        ),
        AppRouter.Config(
            prefix=r'libs/branch/(?P<library_branch_pk>[^/.]+)/feedbacks',
            view=LibraryBranchFeedbackViewSet,
            basename='library-branch-feedback',
        ),
    )
)

urlpatterns = router.urls
