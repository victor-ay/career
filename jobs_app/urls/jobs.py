from rest_framework.routers import DefaultRouter

from jobs_app.views.companies import CompaniesViewSet

router = DefaultRouter()
router.register('', CompaniesViewSet)

urlpatterns = []

urlpatterns.extend(router.urls)