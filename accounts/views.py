from rest_framework.views import APIView
from .serializers import RegistrationSerializer,LoginSerializer,AdminListUserSerializer,UserSearchSerializer
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
                current_site = 'https://gitbase.pythonanywhere.com'
                relative_link = reverse('passwordChange')          
                absurl = current_site + relative_link + "?token="+str(token) 
                email_body = 'Hi ' + user.username + ' Use link below to verify your email and change password \n' + absurl 
                email_subject="Verification Email"
                user.email_user(email_subject,email_body)
                return Response({"status":"created"},status=status.HTTP_201_CREATED)
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)  
    
    def get(self,request):     
        if request.user.is_authenticated:
            if request.user.is_creator:
                users=MyUser.objects.all().exclude(is_superuser=True)
                serializer=AdminListUserSerializer(users,many=True)
                return Response(serializer.data)

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

        
class UserSearchView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            keyword=self.request.GET.get('keyword')
            query=MyUser.objects.filter(username__icontains=keyword).exclude(is_superuser=True)
            serializer=UserSearchSerializer(query,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)  