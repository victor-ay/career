from rest_framework import serializers

from jobs_app.models import ApplicationFlow
from jobs_app.serializers.jobs import JobsSimpleSerializer


class ApplicationsFlowStaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationFlow
        depth = 1
        # fields = '__all__'
        exclude = ('is_deleted',)


class ApplicationsFlowSerializer(serializers.ModelSerializer):
    # job = JobsSimpleSerializer()

    class Meta:
        model = ApplicationFlow
        depth = 1
        # exclude = ( 'is_deleted',)
        exclude = ('to_do',)


class ApplicationsFlowSerializerSimple(serializers.ModelSerializer):
    # job = JobsSimpleSerializer()

    class Meta:
        model = ApplicationFlow
        depth = 0
        # exclude = ('user',)
        exclude = ( 'is_deleted','application')


class ApplicationFlowPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationFlow
        depth = 0
        # fields = '__all__'
        exclude = ('is_deleted',)

class ApplicationsFlowStaffSerializer(serializers.ModelSerializer):
    # job = JobsSimpleSerializer()

    class Meta:
        model = ApplicationFlow
        depth = 1
        exclude = ('user',)
        # exclude = ( 'is_deleted',)
