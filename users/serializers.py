from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

from users.models import Employee, Employer

from collections import OrderedDict


User = get_user_model()


# Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]


class EmployeeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'first_name',
            'last_name',
            'middle_name',
            'about',
            'experience',
        )
        extra_kwargs = {
          'first_name': {'required': True},
          'last_name': {'required': True}
        }


class EmployerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = (
            'name',
            'employee_cnt',
            'address',
            'about'
        )
        extra_kwargs = {
            'name': {'required': True}
        }


# Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password])
    password2 = serializers.CharField(
        write_only=True,
        required=True)

    employee = EmployeeRegisterSerializer(many=False, required=False)
    employer = EmployerRegisterSerializer(many=False, required=False)

    class Meta:
        model = User
        fields = (
            'password',
            'password2',
            'email',
            'user_type',
            'employee',
            'employer')
        extra_kwargs = {
            'user_type': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        match s := sum(1 if attrs.get(attr, None) is not None else 0 for attr in ['employee', 'employer']):
            case _ if s == 0:
                raise serializers.ValidationError(
                    "Specify data for some type of user.")
            case _ if s > 1:
                raise serializers.ValidationError(
                    "Can't specify data for more than one type of users.")
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        for entity in ['employer', 'employee']:
            if validated_data.get(entity, None) is not None:
                entity_kwargs = validated_data.pop(entity)
                break
        print(validated_data)
        user = User.objects.create_user(
            **validated_data,
            **entity_kwargs
        )

        return user

    def to_representation(self, instance):
        result = super().to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])
