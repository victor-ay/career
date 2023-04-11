import copy

import django_filters
from django_filters import FilterSet, BaseInFilter, CharFilter, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from jobs_app.models import Job, FavoriteJobs
from jobs_app.serializers.jobs import JobsStaffSerializer, \
    JobsSimpleSerializer


class JobsPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.id == obj.user_id:
                return True

        return False

class TextInFilter(CharFilter, BaseInFilter):
    pass


class JobsFilterSet(FilterSet):

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')

    job_level = TextInFilter(field_name='job_level')
    employment_type = TextInFilter(field_name='employment_type')
    employment_percent = TextInFilter(field_name='employment_percent')
    job_type = TextInFilter(field_name='job_type')



    class Meta:
        model = Job
        fields = ['title','description','job_level','location']

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5

class JobsViewSet(
                    mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   # mixins.UpdateModelMixin,
                   # mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    queryset = Job.objects.all()
    # serializer_class = JobsSerializer
    permission_classes = [JobsPermissions]
    permission_classes = [IsAuthenticatedOrReadOnly ]



    filter_backends = [DjangoFilterBackend, SearchFilter ,OrderingFilter]
    filterset_class = JobsFilterSet
    ordering_fields = ['job_type', 'job_level', 'employment_percent','posted_on']

    pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return JobsStaffSerializer

        return  JobsSimpleSerializer

    def get_queryset(self):
        super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        user_id = self.request.user.id
        job_id = instance.id

        favorite_last = FavoriteJobs.objects.filter(job=job_id, user=user_id).last()

        if favorite_last:
            favorite = favorite_last.status
        else:
            favorite = False

        serializer = self.get_serializer(instance)

        mydata = copy.deepcopy(serializer.data)
        mydata['favorite'] = favorite

        return Response(mydata)




# class Jobs