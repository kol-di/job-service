from rest_framework import generics

from users.models import Employee, Employer


class EmployeeMenuView(generics.RetrieveAPIView):
    def get_queryset(self):
        employee = Employee.objects.filter(self.kwargs['usr_id'])
        return employee


class EmployerMenuView(generics.RetrieveAPIView):
    def get_queryset(self):
        employer = Employer.objects.filter(self.kwargs['usr_id'])
        return employer