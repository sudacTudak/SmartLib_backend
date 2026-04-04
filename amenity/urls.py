from http_core import AppRouter

from amenity.views import AmenityViewSet

router = AppRouter.from_configs((
    AppRouter.Config(view=AmenityViewSet, basename='amenity'),
))

urlpatterns = router.urls
