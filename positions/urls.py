from http_core import AppRouter, AppRouterConfig
from positions.views import PositionsViewSet

router = AppRouter.from_configs((
    AppRouterConfig(prefix=r'positions', view=PositionsViewSet, basename='positions'),
))

urlpatterns = router.urls