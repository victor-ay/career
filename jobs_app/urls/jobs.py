from rest_framework.routers import DefaultRouter

from jobs_app.views.jobs import JobsViewSet

router = DefaultRouter()




router.register('', JobsViewSet)

urlpatterns = []

urlpatterns.extend(router.urls)