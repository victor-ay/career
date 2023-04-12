from rest_framework import serializers

from jobs_app.models import FavoriteJobs


class FavoriteJobsStaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteJobs
        fields = '__all__'
        depth = 2
        # fields = ['status']

class FavoriteJobsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteJobs
        depth = 2
        # fields = '__all__'
        exclude = ('user',)

class FavoriteJobsPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteJobs
        exclude = ('user',)

