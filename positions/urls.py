from http_core import AppRouter
from positions.views import PositionsViewSet

router = AppRouter.from_configs((
    AppRouter.Config(view=PositionsViewSet, basename='positions'),
))

urlpatterns = router.urls