from http_core import AppRouter
from work_loan.views import WorkLoanViewSet

router = AppRouter.from_configs((
    AppRouter.Config(view=WorkLoanViewSet, basename='work-loan'),
))

urlpatterns = router.urls

