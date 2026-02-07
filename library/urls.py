from library.views import LibraryBranchViewSet
from rest_framework import routers

library_branch_url = 'libs'

router = routers.SimpleRouter()
router.register(fr'{library_branch_url}', LibraryBranchViewSet)


urlpatterns = router.urls