from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_staff')
        # fields = ('email', 'password', 'first_name', 'last_name')


    email = serializers.EmailField (
        write_only= False,
        required = True,
        validators= [UniqueValidator(queryset = User.objects.all())]
    )
    password = serializers.CharField(required=True, write_only=True, allow_null=False, allow_blank=False)
    first_name = serializers.CharField(write_only=False, required=False, allow_blank=True, allow_null=True)
    last_name = serializers.CharField(write_only=False, required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email = validated_data['email'],
            is_staff=validated_data['is_staff'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_staff')

