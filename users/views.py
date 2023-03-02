from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import UserSerializer, EmployeeRegisterSerializer, EmployerRegisterSerializer, RegisterSerializer
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics


User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def who_are_you(request):
    # if request.user.is_active:
    #     return Response({}, template_name='who_are_you.html')
    return Response({}, template_name='who_are_you.html')


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

    renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'register.html'

    def get(self, request, user_type):
        context = {'exclude_fields': ['user_type']}

        match user_type:
            case User.EMPLOYER:
                context['exclude_fields'].append('employee')
            case User.EMPLOYEE:
                context['exclude_fields'].append('employer')

        serializer = RegisterSerializer(context=context)
        return Response({'serializer': serializer}, template_name='register.html')

    def post(self, request, *args, **kwargs):
        print(request)
        serializer = RegisterSerializer(data=request.data)
        print(serializer)
        if not serializer.is_valid():
            return Response({'serializer': serializer}, temaplte_name='vacancies.main_,enu.html')
        serializer.save()
        return HttpResponseRedirect('google.com')


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

