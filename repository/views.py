from django.shortcuts import render
from .serializers import RepositorySerializer,RepositoryCreateSerializer
from .models import Repository,RepositoryContributor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import MyUser
from project.models import Project,ProjectAccess
from subprocess import call
# Create your views here.
class UserRepositoryView(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)  
        repos=[]
        contributors=RepositoryContributor.objects.filter(user_id=request.user)
        for contributor in contributors:
            repos.append(contributor.repo_id)
        serializer=RepositorySerializer(repos,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        serializer = RepositoryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project=serializer.validated_data["project_id"]
        is_manager=ProjectAccess.objects.get(project_id=project,user_id=request.user).is_manager
        if not is_manager:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        serializer.save(created_by=request.user)
        # call(['git-create-repo.sh', request.data['repo_name'], self.request.user.username])
        returnData=serializer.data
        returnData['user_name']=request.user.username
        return Response(returnData, status=status.HTTP_201_CREATED)

class RepositoryDetailView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        repository=Repository.objects.get(id=pk)
        try:
            projectAccess=ProjectAccess.objects.get(user_id=request.user,project_id=repository.project_id)
        except:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        serializer = RepositorySerializer(repository)
        return Response(serializer.data)

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        repository=Repository.objects.get(id=pk)
        try:
            repositoryContributor=RepositoryContributor.objects.get(user_id=request.user,repo_id=repository)
        except:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        serializer = RepositoryCreateSerializer(repository, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        repository=Repository.objects.get(id=pk)
        try:
            projectAccess=ProjectAccess.objects.get(user_id=request.user,project_id=repository.project_id,is_manager=True)
        except:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        # call(['rm', '-rf', f'/var/www/git/{self.request.user.username}/{repository}.git'])
        repository.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   

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
