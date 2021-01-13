from django.contrib.auth import authenticate

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import SignupUserSerializer

class SignupAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupUserSerializer

class LoginAPIView(APIView):
    '''
        for user login 
            params:
                - username
                - password
    '''

    def post(self, request):
        # check if user has entered username and password
        if not request.data.get('username') and not request.data.get('password'):
            return Resonse(
                {'error': 'you have to enter username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        # if user exist
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'username': user.username,
                    'user_type': user.user_type
                }
            )
        # else if user does not exist ...
        else:
            return Response(
                {'error': 'you have entered wrong password or username, please try again'},
                status=status.HTTP_400_BAD_REQUEST
            )