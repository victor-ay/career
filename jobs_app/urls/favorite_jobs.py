from rest_framework.routers import DefaultRouter

from jobs_app.views.favorite_jobs import FavoriteJobsViewSet


router = DefaultRouter()




router.register('', FavoriteJobsViewSet)

urlpatterns = []

urlpatterns.extend(router.urls)