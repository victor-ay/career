from rest_framework import serializers

from jobs_app.models import Contact


class ContactsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'