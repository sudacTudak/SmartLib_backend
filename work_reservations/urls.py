from http_core import AppRouter

from .views import WorkReservationViewSet

router = AppRouter.from_configs((
    AppRouter.Config(view=WorkReservationViewSet, basename='work-reservation'),
))

urlpatterns = router.urls
