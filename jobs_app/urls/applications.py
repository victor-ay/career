from rest_framework.routers import DefaultRouter

from jobs_app.views.applications import ApplicationsViewSet

router = DefaultRouter()
router.register('', ApplicationsViewSet)

urlpatterns = []

urlpatterns.extend(router.urls)