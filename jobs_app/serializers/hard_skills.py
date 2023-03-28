from rest_framework import serializers

from jobs_app.models import HardSkill


class HardSkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = HardSkill
        fields = '__all__'