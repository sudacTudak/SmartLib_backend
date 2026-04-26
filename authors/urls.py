from http_core import AppRouter

from authors.views import AuthorViewSet

router = AppRouter.from_configs(
    (
        AppRouter.Config(prefix='', view=AuthorViewSet, basename='author'),
    ),
)

urlpatterns = router.urls
