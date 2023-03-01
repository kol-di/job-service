from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, EmployeeRegisterSerializer, EmployerRegisterSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics


# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class EmployeeRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmployeeRegisterSerializer

    # model = User
    # form_class = StudentSignUpForm
    # template_name = 'registration/signup_form.html'
    #
    # def get_context_data(self, **kwargs):
    #     kwargs['user_type'] = 'student'
    #     return super().get_context_data(**kwargs)
    #
    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('students:quiz_list')


class EmployerRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmployerRegisterSerializer

    # model = User
    # form_class = StudentSignUpForm
    # template_name = 'registration/signup_form.html'
    #
    # def get_context_data(self, **kwargs):
    #     kwargs['user_type'] = 'student'
    #     return super().get_context_data(**kwargs)
    #
    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('students:quiz_list')

