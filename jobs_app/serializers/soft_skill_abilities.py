from rest_framework import serializers

from jobs_app.models import SoftSkillAbility


class SoftSkillAbilitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SoftSkillAbility
        fields = '__all__'