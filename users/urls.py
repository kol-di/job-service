from django.urls import path
from .views import UserDetailAPI, RegisterUserAPIView, EmployeeRegisterView, EmployerRegisterView


urlpatterns = [
    path('get-details', UserDetailAPI.as_view()),
    path('register', RegisterUserAPIView.as_view()),
    path('register/employee/', EmployeeRegisterView.as_view(), name='employee_register'),
    path('register/employer/', EmployerRegisterView.as_view(), name='employer_register'),
]