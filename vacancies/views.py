from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from users.models import Employee, Employer
from .permissions import EmployeePermission


class EmployeeMenuView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [EmployeePermission]
    renderer_classes = [TemplateHTMLRenderer]

    def get_queryset(self):
        employee = Employee.objects.filter(self.kwargs['usr_id'])
        return employee

    def get(self, request, *args, **kwargs):
        Response({}, template_name='employee_main_menu.html')


class EmployerMenuView(generics.RetrieveAPIView):
    def get_queryset(self):
        employer = Employer.objects.filter(self.kwargs['usr_id'])
        return employer
