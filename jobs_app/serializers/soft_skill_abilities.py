from rest_framework import serializers

from jobs_app.models import HardSkillAbility


class HardSkillAbilitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = HardSkillAbility
        fields = '__all__'