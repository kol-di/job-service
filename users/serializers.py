from rest_framework import serializers
# from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.db.models.deletion import Collector

from users.models import Employee, Employer

from collections import OrderedDict


User = get_user_model()


# Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]


# Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
    user_type = serializers.IntegerField(
        required=True
    )
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

    class Meta:
        model = User
        fields = (
            'password',
            'password2',
            'email',
            # 'first_name',
            # 'last_name',
            'user_type')
        # extra_kwargs = {
        #   'first_name': {'required': True},
        #   'last_name': {'required': True}
        # }

    def validate(self, attrs):
        print(attrs)
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        print(validated_data)
        user = User.objects.create_user(
            **validated_data,
            # email=validated_data['email'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name'],
            # user_type=validated_data['user_type']
        )

        # user.set_password(validated_data['password'])
        # user.save()
        return user

    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except AttributeError:  # overrides default implementation
                for rel_field in ['employee', 'employer']:
                    if (rel_object := getattr(instance, rel_field, None)) is not None:
                        attribute = field.get_attribute(rel_object)
            except SkipField:
                print(field)
                continue

            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret



class EmployeeRegisterSerializer(RegisterSerializer):
    class Meta:
        model = Employee
        fields = (
            'first_name',
            'last_name',
            'middle_name',
            'about',
            'experience',
            'user_type',
            'email',
            'password',
            'password2'
        )


class EmployerRegisterSerializer(RegisterSerializer):
    class Meta:
        model = Employer
        fields = RegisterSerializer.Meta.fields + ('__all__',)

