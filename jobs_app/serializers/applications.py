from rest_framework import serializers

from jobs_app.models import Application


class ApplicationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = '__all__'