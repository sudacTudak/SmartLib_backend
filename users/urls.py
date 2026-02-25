from users.views import AuthViewSet, UsersViewSet
from http_core import AppRouter, AppRouterConfig

auth_url = 'auth'
users_url = 'users'

router = AppRouter.from_configs((
    AppRouterConfig(prefix=fr'{auth_url}', view=AuthViewSet, basename='auth'),
    AppRouterConfig(prefix=fr'{users_url}', view=UsersViewSet, basename='users'),
))

urlpatterns = router.urls
