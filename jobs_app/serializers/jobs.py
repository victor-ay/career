from rest_framework import serializers

from jobs_app.models import Job


# class JobsSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Job
#         fields = '__all__'
#         depth = 1
#
# from jobs_app.serializers.applications import ApplicationPostSerializer
from jobs_app.serializers.auth import UserSerializer
from jobs_app.serializers.companies import CompaniesSerializer
from jobs_app.serializers.favorite_jobs import FavoriteJobsStaffSerializer, FavoriteJobsSerializer


class JobsStaffSerializer(serializers.ModelSerializer):
    company = CompaniesSerializer()
    #
    # def test_new_field(self, obj):
    #     return obj.company.name , obj.company.company_linkedin_url

    class Meta:
        model = Job
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            "source":{"write_only":True},
            "source_job_id": {"write_only": True},
            # "created_at" : {"write_only": True}
        }


class JobsSimpleSerializer(serializers.ModelSerializer):
    company = CompaniesSerializer()
    # applied = ApplicationPostSerializer()

    class Meta:
        model = Job
        # fields = '__all__'
        depth = 1
        exclude = ['favorited_by_user', 'created_at', 'applicants', 'recruiter', 'closed_at']
        # exclude = ['favorited_by_user', 'created_at', 'recruiter', 'closed_at']
        extra_kwargs = {
            "source":{"write_only":True},
            "source_job_id": {"write_only": True},
        }

