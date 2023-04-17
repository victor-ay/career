import copy

from rest_framework import mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from jobs_app.models import Application, ApplicationFlow
from jobs_app.serializers.application_flow import ApplicationsFlowSerializer, ApplicationsFlowStaffSerializer, \
    ApplicationFlowPostSerializer


class ApplicationsFlowPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST']:
            application_qs = Application.objects.filter(id=request.data['application'], user=request.user.id)
            return len(application_qs)>0
        return True

    def has_object_permission(self, request, view, obj):

        if request.method in ['PATCH','PUT','DELETE']:
            application_qs = Application.objects.filter(id=obj.application_id, user=obj.application.user_id)
            return len(application_qs) > 0


class ApplicationsFlowSet(
                    mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet
                    ):
    queryset = ApplicationFlow.objects.all()
    permission_classes = [IsAuthenticated, ApplicationsFlowPermissions]
    # serializer_class = ApplicationsSerializer

    def get_queryset(self):
        super().get_queryset()
        if not self.request.user.is_staff:
            qs = self.queryset.filter(application__user=self.request.user.id, is_deleted=False)
            return qs
        return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.request.user.is_staff:
                return ApplicationsFlowStaffSerializer
            return ApplicationsFlowSerializer
        else:
            return ApplicationFlowPostSerializer


    def return_null_or_data(self,field):
        if self.request.data.get(field):
            return self.request.data.get(field)
            # return field
        return None

    def validate_application_exists(self):
        status = self.request.data['status']
        # notes = self.request.data['notes']
        # to_do_date = self.request.data['to_do_date']
        # to_do = self.request.data['to_do']
        notes = self.return_null_or_data('notes')
        to_do_date = self.return_null_or_data('to_do_date')
        to_do = self.return_null_or_data('to_do')
        application = self.return_null_or_data('application')


        user_id= self.request.user.id
        application_qs = ApplicationFlow.objects.filter(application__user=user_id,
                                                       application=application,
                                                       status=status,
                                                       notes = notes,
                                                       to_do_date = to_do_date,
                                                       to_do = to_do)

        if application_qs:
            raise ValidationError(
                    f"Not Unique! This type of update exists already : status = <{status}> , notes = <{notes}> , to_do_date = <{to_do_date}>, to_do = <{to_do}> ")
    #
    # def validate_has_permission_for_application_id(self):
    #     application_qs = Application.objects.filter(id = self.request.data['application'])

    def create(self, request, *args, **kwargs):

        self.validate_application_exists()
        my_request_data = copy.deepcopy(request.data)

        # ???
        # my_request_data['application'] = self.request.data[]

        serializer = self.get_serializer(data=my_request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        instance.is_deleted= True
        instance.save()

