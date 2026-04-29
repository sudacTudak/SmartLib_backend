from works.views import WorkViewSet, GenreViewSet, WorkItemViewSet
from http_core import AppRouter

genre_url = 'genre'
work_items_url = 'work-items'

router = AppRouter.from_configs((
    AppRouter.Config(view=WorkViewSet),
    AppRouter.Config(prefix=fr'{genre_url}', view=GenreViewSet),
    AppRouter.Config(prefix=fr'{work_items_url}', view=WorkItemViewSet),
))

urlpatterns = router.urls

