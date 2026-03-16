from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.urls import path
from users.views import AuthViewSet, UsersViewSet, StaffViewSet
from http_core import AppRouter

auth_url = 'auth'
users_url = ''
staff_url = 'staff'
token_url = 'token'

router = AppRouter.from_configs((
    AppRouter.Config(prefix=fr'{auth_url}', view=AuthViewSet, basename='auth'),
    AppRouter.Config(prefix=fr'{staff_url}', view=StaffViewSet, basename='staff'),
    AppRouter.Config(view=UsersViewSet, basename='users'),
))

urlpatterns = [
                  path(f'{auth_url}/{token_url}/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
              ] + router.urls
