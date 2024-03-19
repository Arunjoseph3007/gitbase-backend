from django.shortcuts import render
from .serializers import RepositorySerializer
from .models import Repository,RepositoryContributor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import MyUser
# Create your views here.
class UserRepositoryView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            repos=[]
            contributors=RepositoryContributor.objects.filter(user_id=request.user)
            for contributor in contributors:
                repos.append(contributor.repo_id)
            serializer=RepositorySerializer(repos,many=True)
            return Response(serializer.data)
        return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)  

class UserProfileRepository(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_creator:
                username=request.GET.get("username")
                user=MyUser.objects.get(username=username)
                contributors=RepositoryContributor.objects.filter(user_id=user)
                repos=[]
                for contributor in contributors:
                    repos.append(contributor.repo_id)
                serializer=RepositorySerializer(repos,many=True)
                return Response(serializer.data)
        return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)          
