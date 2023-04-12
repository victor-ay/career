from rest_framework.routers import DefaultRouter
from django.urls import path, include

from jobs_app.views.jobs import JobsViewSet

router = DefaultRouter()




router.register('', JobsViewSet)

urlpatterns = [

]

urlpatterns.extend(router.urls)