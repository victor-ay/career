from rest_framework import serializers

from jobs_app.models import Company


class CompaniesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        # fields = '__all__'
        exclude = ['user', 'company_id_linkedin', 'list_my_jobs']