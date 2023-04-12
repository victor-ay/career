import copy

from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from jobs_app.models import FavoriteJobs
from jobs_app.serializers.companies import CompaniesSerializer
from jobs_app.serializers.favorite_jobs import FavoriteJobsSerializer, FavoriteJobsStaffSerializer, \
    FavoriteJobsPostSerializer
from jobs_app.serializers.jobs import JobsSimpleSerializer

class FavoriteDeletePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.id == obj.user_id

class FavoriteJobsViewSet(
                    mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   # mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    queryset = FavoriteJobs.objects.all()
    # serializer_class = FavoriteJobsSerializer
    permission_classes = [IsAuthenticated, FavoriteDeletePermission]




    def get_queryset(self):
        super().get_queryset()
        if not self.request.user.is_staff:
            qs = self.queryset.filter(user=self.request.user.id)
            return qs
        return self.queryset

    def get_serializer_class(self):
        # super().get_serializer_class()
        if self.request.method == 'POST':
            serializer_class = FavoriteJobsPostSerializer
            return serializer_class

        if self.request.user.is_staff:
            serializer_class = FavoriteJobsStaffSerializer
        else:
            serializer_class = FavoriteJobsSerializer

        return serializer_class

    def perform_create(self, serializer):
        user_id = self.request.user.id
        job_id =self.request.data['job']
        qs = FavoriteJobs.objects.filter(job=job_id,user=user_id)

        if len(qs)>0:
            raise ValidationError(f"Not Unique! The job #<{job_id}> already in favorites of user <{self.request.user.username}>")
        serializer.validated_data['user'] = self.request.user

        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def list(self, request, *args, **kwargs):

        # List of elements to be removed from the data
        list_to_pop = ["favorited_by_user", "applicants","recruiter","closed_at","created_at"]
        list_to_pop_company = ["list_my_jobs", "user"]

        user_id = self.request.user.id
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            # Making copy of the data to be changed before responding to API
            mydata = copy.deepcopy(serializer.data)

            # Going through the list of the response

            for i in range (len(mydata)):
                job = mydata[i]['job']
                job_id = job['id']

                # Removing unwanted elements from the job (level 0)
                for pop_elem in list_to_pop:
                    job.pop(pop_elem)

                for pop_elem_comp in list_to_pop_company:
                    job['company'].pop(pop_elem_comp)

            return self.get_paginated_response(mydata)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)