from http_core import AppRouter, AppRouterConfig
from library.views import LibraryBranchViewSet

library_branch_url = 'branch'

router = AppRouter.from_configs((
    AppRouterConfig(prefix=fr'{library_branch_url}', view=LibraryBranchViewSet),
))

urlpatterns = router.urls
