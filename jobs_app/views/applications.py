import copy

from rest_framework import mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from jobs_app.models import Application
from jobs_app.serializers.applications import ApplicationsSerializer, ApplicationsStaffSerializer, \
    ApplicationPostSerializer


# class ApplicationsPermissions(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in ['GET'] and request.user.is_staff:
#             return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         pass


class ApplicationsViewSet(
                    mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet
                    ):
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]
    # serializer_class = ApplicationsSerializer

    def get_queryset(self):
        super().get_queryset()
        if not self.request.user.is_staff:
            qs = self.queryset.filter(user=self.request.user.id)
            return qs
        return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.request.user.is_staff:
                return ApplicationsStaffSerializer
            return ApplicationsSerializer
        else:
            return ApplicationPostSerializer

    def validate_application_exists(self):
        job_id = self.request.data['job']
        user_id= self.request.user.id
        applicatio_qs = Application.objects.filter(user=user_id,job=job_id)

        if applicatio_qs:
            raise ValidationError(
                    f"Not Unique! The job #<{job_id}> already in favorites of user <{self.request.user.username}>")

    def create(self, request, *args, **kwargs):

        self.validate_application_exists()
        my_request_data = copy.deepcopy(request.data)
        my_request_data['user'] = self.request.user.id

        serializer = self.get_serializer(data=my_request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        instance.is_deleted= True
        instance.save()

