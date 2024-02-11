from rest_framework.views import APIView
from .serializers import RegistrationSerializer,LoginSerializer,ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import update_session_auth_hash
from .models import MyUser
from django.urls import reverse
# from django.contrib.sites.models import Site
# Create your views here.

class RegistrationView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            if request.user.is_creator:
                serializer=RegistrationSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user=serializer.save()
                token = Token.objects.get(user = user).key
                current_site = 'http://localhost:8000'
                relative_link = reverse('passwordChange')          
                absurl = current_site + relative_link + "?token="+str(token) 
                email_body = 'Hi ' + user.username + ' Use link below to verify your email and change password \n' + absurl 
                email_subject="Verification Email"
                user.email_user(email_subject,email_body)
                return Response({"status":"created"},status=status.HTTP_201_CREATED)
            else:
                return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)       
        else:
            return Response({"error":"Admin login required"},status=status.HTTP_401_UNAUTHORIZED)

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=MyUser.objects.get(email=serializer.validated_data['email'])
        token=Token.objects.get(user=user)
        return Response(token.key,status=status.HTTP_200_OK)

# class verifyEmail(APIView):
#     def get(self,request):
#         data = {}
#         token = request.GET.get('token')
#         try:
#             user = MyUser.objects.get(auth_token = token)
#         except:
#             content = {'detail': 'User already activated!'}
#             return Response(content)
#         if user.is_active == False:
#             user.is_active = True
#             user.save()
#             Token.objects.get(user = user).delete()
#             Token.objects.create(user = user)
#             new_token = Token.objects.get(user = user).key   
#             content = {'detail': 'Email verified!'}  
#             return Response(content)
#         else:
#             content={'status':'Email Not Verified'}
#             return Response(content)


class ChangePasswordView(APIView):
    def post(self,request):
        token = request.GET.get('token')
        new_password = request.POST.get('new_password')
        user = MyUser.objects.get(auth_token = token)
        user=Token.objects.get(key=token).user
        user.set_password(new_password)
        if user.is_active == False:
            user.is_active = True
        user.save()
        Token.objects.get(user=user).delete()
        Token.objects.create(user=user)
        update_session_auth_hash(request, user)
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)

# class ChangePasswordEmailView(APIView):
#     def post(self,request):
#         user=request.user
#         subject="Password Reset for Gitbase"
#         current_domain=Site.objects.get_current().domain
#         print(current_domain)
#         relative_link='change_password'
#         user_token=Token.objects.get(user=user)
#         link=current_domain+relative_link+"?token="+user_token
#         message=f"Here is your link for password reset:\n{link}"
#         user.email_user(subject,message)
