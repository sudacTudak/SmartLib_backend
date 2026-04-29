from http_core import AppRouter

from feedback.views import WorkFeedbackViewSet, LibraryBranchFeedbackViewSet

router = AppRouter.from_configs(
    (
        AppRouter.Config(
            prefix=r'works',
            view=WorkFeedbackViewSet,
            basename='work-feedback',
        ),
        AppRouter.Config(
            prefix=r'libs',
            view=LibraryBranchFeedbackViewSet,
            basename='library-branch-feedback',
        ),
    )
)

urlpatterns = router.urls
