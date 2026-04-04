from amenity.views.amenity_vendor import AmenityVendorViewSet
from http_core import AppRouter

from amenity.views.amenity import AmenityViewSet

router = AppRouter.from_configs((
    AppRouter.Config(view=AmenityVendorViewSet, prefix='vendors', basename='amenity_vendors'),
    AppRouter.Config(view=AmenityViewSet, basename='amenity'),
))

urlpatterns = router.urls
