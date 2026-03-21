from http_core import AppRouter

from suppliers.views import SupplierViewSet

router = AppRouter.from_configs((
    AppRouter.Config(view=SupplierViewSet),
))

urlpatterns = router.urls

