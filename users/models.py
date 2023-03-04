from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from .exceptions import UnknownUserType


class MyAccountManager(BaseUserManager):
    def create_user(self, password=None, **params):
        user_type = params['user_type']

        match user_type:
            case self.model.EMPLOYEE:
                user = Employee(**params)
            case self.model.EMPLOYER:
                user = Employer(**params)
            case _:
                raise UnknownUserType(user_type)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True, null=True, default=None)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    EMPLOYER = 1
    EMPLOYEE = 2
    ADMIN = 3
    USER_TYPE_CHOICES = (
        (EMPLOYER, 'employer'),
        (EMPLOYEE, 'employee'),
        (ADMIN, 'admin'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return str(self.email)


class Employee(User):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    middle_name = models.CharField(max_length=30, blank=True)
    about = models.TextField(max_length=500, blank=True)
    experience = models.TextField(max_length=500, blank=True)

    class Meta:
        permissions = (('employee', 'Is employee'),)


class Employer(User):
    name = models.CharField(max_length=50, blank=False)
    employee_cnt = models.PositiveIntegerField(blank=True, null=True)
    address = models.TextField(max_length=50, blank=True)
    about = models.TextField(max_length=500, blank=True)

    class Meta:
        permissions = (('employer', 'Is employer'),)
