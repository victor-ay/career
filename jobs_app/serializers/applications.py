from rest_framework import serializers

from jobs_app.models import Application
from jobs_app.serializers.application_flow import ApplicationsFlowSerializer, ApplicationsFlowSerializerSimple, \
    ApplicationsFlowStaffSerializer
from jobs_app.serializers.companies import CompaniesSerializer
from jobs_app.serializers.jobs import JobsSimpleSerializer


class ApplicationsStaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        depth = 1
        # fields = '__all__'
        exclude = ('is_deleted',)


class ApplicationsSerializer(serializers.ModelSerializer):
    job = JobsSimpleSerializer()
    # application_flows =ApplicationsFlowSerializerSimple(many=True)
    application_flows = ApplicationsFlowSerializer(many=True)

    class Meta:
        model = Application
        depth = 0
        # exclude = ('user',)
        exclude = ('user', 'is_deleted',)



class ApplicationPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        depth = 0
        # fields = '__all__'
        exclude = ('is_deleted',)




