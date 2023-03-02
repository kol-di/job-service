from django.urls import path
from .views import UserDetailAPI, RegisterUserAPIView, who_are_you


urlpatterns = [
    path('get-details', UserDetailAPI.as_view()),
    # path('register/', RegisterUserAPIView.as_view(), name='who_are_you'),
    path('register/', who_are_you, name='who-are-you'),
    path('register/<int:user_type>/', RegisterUserAPIView.as_view(), name='register-form'),
]