from rest_framework import serializers

from jobs_app.models import SoftSkill


class SoftSkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SoftSkill
        fields = '__all__'