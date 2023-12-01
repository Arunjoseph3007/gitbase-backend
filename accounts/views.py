from rest_framework.views import APIView
from .serializers import RegistrationSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
# Create your views here.

class RegistrationView(APIView):
    def post(self, request):
        #Validate serializer fields
        serializer=RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data=serializer.validated_data
        #Create user and his token
        user=MyUser.objects.create_user(valid_data['username'],valid_data['email'],valid_data['password'])
        Token.objects.create(user=user)
        #Return response
        return Response({"status":"created"},status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self,request):
        #Validate serializer fields
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data=serializer.data
        #Authenticate the user
        user = authenticate(email=valid_data['email'], password=valid_data['password'])
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        #Retrive his token
        token=Token.objects.get(user=user)
        return Response(token.key,status=status.HTTP_200_OK)


        
