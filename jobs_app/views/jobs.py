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

from jobs_app.models import Job, FavoriteJobs, Application
from jobs_app.serializers.jobs import JobsStaffSerializer, \
    JobsSimpleSerializer


class JobsPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True

        if request.method in ['POST'] and request.user and request.user.is_staff:
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
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
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

    # permission_classes = [IsAuthenticatedOrReadOnly, JobsPermissions ]
    permission_classes = [IsAuthenticatedOrReadOnly]



    filter_backends = [DjangoFilterBackend, SearchFilter ,OrderingFilter]
    filterset_class = JobsFilterSet
    ordering_fields = ['job_type', 'job_level', 'employment_percent','posted_on']
    ordering = ['-posted_on']

    pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return JobsStaffSerializer

        return  JobsSimpleSerializer

    def get_queryset(self):
        super().get_queryset()


    # def create(self, request, *args, **kwargs):
    #     if

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        user_id = self.request.user.id
        job_id = instance.id

        favorite_qs = FavoriteJobs.objects.filter(job=job_id, user=user_id)
        favorite = len(favorite_qs)>0

        applied_qs = Application.objects.filter(job=job_id, user=user_id)
        applied = len(favorite_qs)>0

        serializer = self.get_serializer(instance)

        mydata = copy.deepcopy(serializer.data)
        mydata['favorite'] = favorite
        mydata['applied'] = applied


        return Response(mydata)

    @staticmethod
    def add_favorite_and_applied_field( serialized_data, users_favorite_jobs, users_applied_jobs):
        mydata = copy.deepcopy(serialized_data)
        for i in range(len(mydata)):
            mydata[i]['favorite'] = mydata[i]['id'] in users_favorite_jobs
            mydata[i]['applied'] = mydata[i]['id'] in users_applied_jobs

        return mydata

    @staticmethod
    def add_applied_field( serialized_data, users_applied_jobs):
        mydata = copy.deepcopy(serialized_data)
        for i in range(len(mydata)):
            mydata[i]['applied'] = mydata[i]['id'] in users_applied_jobs

        return mydata

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().list(self, request, *args, **kwargs)
        else:
            user_id = self.request.user.id
            favorite_qs = FavoriteJobs.objects.filter(user=user_id)
            users_favorite_jobs=[]
            for fav in favorite_qs:
                users_favorite_jobs.append(fav.job_id)

            applicants_qs = Application.objects.filter(user=user_id)
            users_applied_jobs=[]
            for appl in applicants_qs:
                users_applied_jobs.append(appl.job_id)

            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)

                # mydata = copy.deepcopy(serializer.data)
                # for i in range(len(mydata)):
                #     mydata[i]['favorite'] = mydata[i]['id'] in users_favorite_jobs

                mydata = self.add_favorite_and_applied_field(serialized_data=serializer.data ,
                                                             users_favorite_jobs = users_favorite_jobs,
                                                             users_applied_jobs = users_applied_jobs)

                return self.get_paginated_response(mydata)

            serializer = self.get_serializer(queryset, many=True)
            mydata = self.add_favorite_and_applied_field(serialized_data=serializer.data,
                                                         users_favorite_jobs=users_favorite_jobs,
                                                         users_applied_jobs = users_applied_jobs)
            # return Response(serializer.data)
            return Response(mydata)







# class Jobs