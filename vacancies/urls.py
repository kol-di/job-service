from django.urls import path

from .views import EmployeeMenuView, EmployerMenuView


urlpatterns = [
    path('employee_menu/<int:user_id>', EmployeeMenuView.as_view(), name='employee-menu'),
    path('employer_menu/<int:user_id>', EmployerMenuView.as_view(), name='employer-menu'),
]