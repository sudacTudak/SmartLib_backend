from http_core import AppRouter

from inventory_movement.views import InventoryMovementViewSet

inventory_movement_url = 'movements'

router = AppRouter.from_configs((
    AppRouter.Config(prefix=fr'{inventory_movement_url}', view=InventoryMovementViewSet),
))

urlpatterns = router.urls

