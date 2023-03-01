from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser


class MyAccountManager(BaseUserManager):
    # def create_user(self, email, first_name, last_name, user_type, password=None, **params):
    def create_user(self, password=None, **params):
        email = params.pop('email')
        user_type = params.pop('user_type')

        if not email:
            raise ValueError('Users must have an email address')

        print('CREATING USER')
        user = self.model(
            email=self.normalize_email(email),
            # first_name=first_name,
            # last_name=last_name,
            user_type=user_type
        )
        user.set_password(password)
        user.save(using=self._db)
        print('CREATED USER')

        match user_type:
            case self.model.EMPLOYEE:
                employee = Employee(
                    user=user,
                    **params
                )
                employee.save()
            case self.model.EMPLOYER:
                employer = Employer(
                    user=user,
                    **params
                )
                employer.save()
        print(employee.middle_name)
        print('EXIT CREATE USER')

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
    # first_name = models.CharField(max_length=30, blank=False)
    # last_name = models.CharField(max_length=30, blank=False)
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

    # class Meta:
    #     db_table = "tbl_users"

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    middle_name = models.CharField(max_length=30, blank=True)
    about = models.TextField(max_length=500, blank=True)
    experience = models.TextField(max_length=500, blank=True)


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    employee_cnt = models.PositiveIntegerField(blank=True)
    address = models.TextField(max_length=50, blank=True)
    about = models.TextField(max_length=500, blank=True)
