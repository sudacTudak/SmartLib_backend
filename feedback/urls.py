from http_core import AppRouter

from feedback.views import BookBasisFeedbackViewSet, LibraryBranchFeedbackViewSet

router = AppRouter.from_configs(
    (
        AppRouter.Config(
            prefix=r'book-bases',
            view=BookBasisFeedbackViewSet,
            basename='book-basis-feedback',
        ),
        AppRouter.Config(
            prefix=r'libs',
            view=LibraryBranchFeedbackViewSet,
            basename='library-branch-feedback',
        ),
    )
)

urlpatterns = router.urls
