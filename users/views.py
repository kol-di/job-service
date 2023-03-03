from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect, QueryDict
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.reverse import reverse

from itertools import chain

from .serializers import UserSerializer, RegisterSerializer
from .utils import nested_dict_values
from .exceptions import UnknownUserType


User = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def who_are_you(request):
    return Response({}, template_name='who_are_you.html')


# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        print(request.user)
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, user_type):
        context = {'exclude_fields': ['user_type']}

        match user_type:
            case User.EMPLOYER:
                context['exclude_fields'].append('employee')
                template_name = 'register_employer.html'
            case User.EMPLOYEE:
                context['exclude_fields'].append('employer')
                template_name = 'register_employee.html'
            case _:
                raise UnknownUserType(user_type)

        serializer = RegisterSerializer(context=context)
        return Response({'serializer': serializer}, template_name=template_name)

    def post(self, request, *args, **kwargs):
        # append user_type to the request
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data.update({'user_type': kwargs['user_type']})

        serializer = RegisterSerializer(data=request.data, context=kwargs)
        if not serializer.is_valid():
            errors = list(chain(*nested_dict_values(serializer.errors)))    # get all error strings
            request.session['errors'] = errors
            return HttpResponseRedirect(request.path)
        user = serializer.save()

        match kwargs['user_type']:
            case User.EMPLOYEE:
                url = reverse('employee-menu', kwargs={'user_id': user.id})
            case User.EMPLOYER:
                url = reverse('employer-menu', kwargs={'user_id': user.id})
            case _:
                raise UnknownUserType(kwargs['user_type'])
        return HttpResponseRedirect(url)
