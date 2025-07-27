from django.shortcuts import render
from .serializers import RepositorySerializer,RepositoryCreateSerializer,AddContributorSerializer,GetContributorSerializer,GetUserRepositorySerializer,MyUserSerializer,StarRepoSerializer,RecentContributionSerializer
from .models import Repository,RepositoryContributor,Star_Repo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import MyUser
from project.models import Project,ProjectAccess
from subprocess import call
from project.serializers import ProjectListSerializer
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
        data=serializer.validated_data
        print(data)
        project=Project.objects.get(project_name=data["project_name"])
        try:
            ProjectAccess.objects.get(project_id=project,user_id=request.user,is_manager=True)
        except:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        repository=Repository.objects.create(created_by=request.user,project_id=project,repo_name=data["repo_name"],repo_description=data["repo_description"])
        RepositoryContributor.objects.create(repo_id=repository,user_id=request.user)
        call(['git-create-repo.sh', request.data['repo_name'], self.request.user.username])
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
        # call(['rm', '-rf', f'/var/www/git/{request.user.username}/{repository}.git'])
        repository.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   

class AddContributorView(APIView):
    def post(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        serializer=AddContributorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=serializer.validated_data
        project=Project.objects.get(project_name=data["project_name"])
        repository=Repository.objects.get(project_id=project,repo_name=data["repo_name"])
        is_manager=ProjectAccess.objects.get(project_id=project,user_id=request.user).is_manager
        if not is_manager:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        try:
            ProjectAccess.objects.get(project_id=project,user_id=serializer.validated_data["user_id"])
        except:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        RepositoryContributor.objects.create(repo_id=repository,user_id=data["user_id"])
        return Response(serializer.data)

    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        reponame=self.request.GET.get('reponame')
        project_name=self.request.GET.get('project_name')
        project=Project.objects.get(project_name=project_name)
        try:
            project_access=ProjectAccess.objects.get(project_id=project,user_id=request.user)
        except:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        repository=Repository.objects.get(project_id=project,repo_name=reponame)
        query=RepositoryContributor.objects.filter(repo_id=repository)
        serializer=GetContributorSerializer(query,many=True)
        return Response(serializer.data)

class ContributorDetailView(APIView):
    def get(self,request,pk):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        contributor=RepositoryContributor.objects.get(id=pk)
        project=contributor.repo_id.project_id
        try:
            project_access=ProjectAccess.objects.get(project_id=project,user_id=request.user)
        except:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        serializer=GetContributorSerializer(contributor)
        return Response(serializer.data)

    def delete(self, request,pk):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        contributor=RepositoryContributor.objects.get(id=pk)
        project=contributor.repo_id.project_id
        try:
            project_access=ProjectAccess.objects.get(project_id=project,user_id=request.user)
        except:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        contributor.delete()
        return Response("Contributor Deleted")

class GetUserRepos(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        print("Here")
        username=request.GET.get('username')  
        user=MyUser.objects.get(username=username)
        queryset=RepositoryContributor.objects.filter(user_id=user)
        repositoryList=[]
        for contribution in queryset:
            repositoryList.append(contribution.repo_id)
        project_access=ProjectAccess.objects.filter(user_id=request.user)
        projectList=[]
        for access in project_access:
            projectList.append(access.project_id)
        response=[]
        for repo in repositoryList:
            if repo.project_id in projectList:
                response.append(repo)
        repo_serializer=GetUserRepositorySerializer(response,many=True)    
        user_serializer = MyUserSerializer(user) 
        project_serializer=ProjectListSerializer(projectList,many=True)
        print(user_serializer)
        responseData = {
            'UserDetails': user_serializer.data,
            'RepoDetails': repo_serializer.data,
            'ProjectDetails':project_serializer.data
        }
        print(responseData)
        return Response(responseData)
         
        
class RepoSearch(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        query=request.GET.get('repo')             
        userrepos=Repository.objects.filter(repo_name__icontains=query)
        project_access=ProjectAccess.objects.filter(user_id=request.user)
        projectList=[]
        for access in project_access:
            projectList.append(access.project_id)
        response=[]
        for repo in userrepos:
            if repo.project_id in projectList:
                response.append(repo)
        repo_serializer=RepositorySerializer(response,many=True)
        return Response(repo_serializer.data)

class StarRepoView(APIView):
    def post(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        repo_name=request.GET.get('repo_name')
        project_name=request.GET.get('project_name')
        repo_obj=Repository.objects.get(repo_name=repo_name,project_id__project_name=project_name)
        try:
            ProjectAccess.objects.get(project_id__project_name=project_name,user_id=request.user)
        except:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        Star_Repo.objects.create(star_repo=repo_obj,star_by=request.user)
        return Response("Repo Starred")

    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        qs=Star_Repo.objects.filter(star_by=request.user)
        serializer=StarRepoSerializer(qs,many=True)
        return Response(serializer.data)

class StarRepoDetail(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        repo_name=request.GET.get('repo_name')
        project_name=request.GET.get('project_name')        
        repo_obj=Repository.objects.get(repo_name=repo_name,project_id__project_name=project_name)
        try:
            star=Star_Repo.objects.get(star_by=request.user,star_repo=repo_obj)
            return Response({'is_starred':True})
        except:
            return Response({'is_starred':False})

    def delete(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        repo_name=request.GET.get('repo_name')
        project_name=request.GET.get('project_name')     
        repo_obj=Repository.objects.get(repo_name=repo_name,project_id__project_name=project_name)   
        star=Star_Repo.objects.get(star_by=request.user,star_repo=repo_obj)
        star.delete()
        return Response("Repo Unstarred")

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

class RecentContributionView(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        query=RepositoryContributor.objects.filter(user_id=request.user)
        response=[]
        for contribution in query:
            response.append(contribution.repo_id)
        serializer=RecentContributionSerializer(response,many=True)
        return Response(serializer.data)