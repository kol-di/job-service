from rest_framework.permissions import DjangoModelPermissions, BasePermission
from django.core.exceptions import PermissionDenied


class EmployeePermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user.is_authenticated)
        print(request.user)

        if request.user.is_authenticated and \
                request.user.has_perm('Employee.employee'):
            return True
        raise PermissionDenied()
