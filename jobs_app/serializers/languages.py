from rest_framework import serializers

from jobs_app.models import Language


class LanguagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'