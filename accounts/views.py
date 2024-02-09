from rest_framework.views import APIView
from .serializers import RegistrationSerializer,LoginSerializer,ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import update_session_auth_hash
from .models import MyUser
# from django.contrib.sites.models import Site
# Create your views here.

class RegistrationView(APIView):
    def post(self, request):
        # if request.user.is_creator:
            serializer=RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status":"created","data":serializer.data},status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=MyUser.objects.get(email=serializer.validated_data['email'])
        token=Token.objects.get(user=user)
        return Response(token.key,status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    def post(self,request):
        token = request.GET.get('token')
        serializer=ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data=serializer.data
        user=Token.objects.get(key=token).user
        if user.check_password(valid_data['old_password']):
            user.set_password(valid_data['new_password'])
            user.save()
            Token.objects.get(user=user).delete()
            Token.objects.create(user=user)
            update_session_auth_hash(request, user)
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordEmailView(APIView):
    def post(self,request):
        user=request.user
        subject="Password Reset for Gitbase"
        current_domain=Site.objects.get_current().domain
        print(current_domain)
        relative_link='change_password'
        user_token=Token.objects.get(user=user)
        link=current_domain+relative_link+"?token="+user_token
        message=f"Here is your link for password reset:\n{link}"
        user.email_user(subject,message)
