from rest_framework.routers import DefaultRouter

from jobs_app.views.application_flow import ApplicationsFlowSet

router = DefaultRouter()
router.register('', ApplicationsFlowSet)

urlpatterns = []

urlpatterns.extend(router.urls)