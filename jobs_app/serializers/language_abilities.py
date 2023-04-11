from rest_framework import serializers

from jobs_app.models import LanguageAbility


class LanguageAbilitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = LanguageAbility
        fields = '__all__'