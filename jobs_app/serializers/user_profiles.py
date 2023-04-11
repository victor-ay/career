from rest_framework import serializers

from jobs_app.models import UserProfile


class UserProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'