import copy

from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from jobs_app.models import FavoriteJobs
from jobs_app.serializers.favorite_jobs import FavoriteJobsSerializer, FavoriteJobsStaffSerializer, \
    FavoriteJobsPostSerializer
from jobs_app.serializers.jobs import JobsSimpleSerializer


class FavoriteJobsViewSet(
                    mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   # mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    queryset = FavoriteJobs.objects.all()
    serializer_class = FavoriteJobsSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly ]


    def get_queryset(self):
        super().get_queryset()
        if not self.request.user.is_staff:
            qs = self.queryset.filter(user=self.request.user.id, status = True)
            return qs
        return self.queryset

    def retrieve(self, request, *args, **kwargs):
        super().retrieve()

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

    def list(self, request, *args, **kwargs):

        # List of elements to be removed from the data
        list_to_pop = ["favorited_by_user", "applicants","recruiter","closed_at","created_at"]
        # list_to_pop = [ "applicants", "recruiter", "closed_at", "created_at"]

        mydata_export = []

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

                # Requesting the last favorite record

                # if job["favorited_by_user"]
                favorite_last = FavoriteJobs.objects.filter(job=job_id, user=user_id).last()
                if favorite_last:
                    favorite = favorite_last.status
                else:
                    favorite = False

                if favorite:
                    job['favorite'] = favorite
                    mydata[i]['job'] = job
                    if isinstance(mydata[i]['job']["company"], dict):
                        mydata[i]['job']["company"].pop("user")
                        mydata[i]['job']["company"].pop("list_my_jobs")
                    mydata_export.append(mydata[i])

            # for j in remove_not_favorites:

            return self.get_paginated_response(mydata_export)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)