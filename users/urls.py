from users.views import AuthViewSet, UsersViewSet, StaffViewSet
from http_core import AppRouter, AppRouterConfig

auth_url = 'auth'
users_url = ''
staff_url = 'staff'

router = AppRouter.from_configs((
    AppRouterConfig(prefix=fr'{auth_url}', view=AuthViewSet, basename='auth'),
    AppRouterConfig(prefix=fr'{staff_url}', view=StaffViewSet, basename='staff'),
    AppRouterConfig(prefix=fr'', view=UsersViewSet, basename='users'),
))

urlpatterns = router.urls
