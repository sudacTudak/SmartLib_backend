from http_core import AppRouter

from reports.views import ReportsViewSet

router = AppRouter.from_configs((AppRouter.Config(prefix='reports', view=ReportsViewSet),))

urlpatterns = router.urls
