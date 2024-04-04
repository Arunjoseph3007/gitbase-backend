from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ProjectListSerializer,ProjectCreateSerializer,GetProjectAccessSerializer,PostProjectAccessSerializer,UpdateProjectAccessSerializer
from .models import Project,ProjectAccess
from accounts.models import MyUser
from rest_framework.response import Response
from repository.models import Repository
from repository.serializers import RepositorySerializer
from rest_framework import status
# Create your views here.
class AdminProjectsCreateView(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_creator:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        projects=Project.objects.all()
        serializer=ProjectListSerializer(projects,many=True)
        return Response(serializer.data)

    def post(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_creator:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        user=request.user
        serializer=ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        projectInstance=serializer.save(created_by=user)
        ProjectAccess.objects.create(project_id=projectInstance,user_id=user,is_manager=True)
        return Response(serializer.data)

class AdminProjectsUpdateView(APIView): 
    def put(self,request,pk):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED) 
        if not request.user.is_creator:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        project_description=request.POST.get('project_description')
        project=Project.objects.get(id=pk)
        project.project_description=project_description
        project.save()
        serializer=ProjectCreateSerializer(project)
        return Response(serializer.data)   
    
    def delete(self,request,pk):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED) 
        if not request.user.is_creator:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED) 
        Project.objects.get(id=pk).delete()   
        return Response({"status":"Project deleted"})

class UserProjectsListView(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        projects=[]
        projectAccess=ProjectAccess.objects.filter(user_id=request.user)
        for project in projectAccess:
            projects.append(Project.objects.get(id=project.project_id.id))
        serializer=ProjectListSerializer(projects,many=True)
        return Response(serializer.data)

def str2bool(str):
    return True if str=="true" else False

class AdminProvideProjectAccess(APIView):
    def post(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_creator:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED) 
        serializer=PostProjectAccessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=serializer.validated_data
        project=Project.objects.get(project_name=data["project_name"])
        if not project.created_by==request.user:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)         
        ProjectAccess.objects.create(user_id=data["user_id"],project_id=project,is_manager=data["is_manager"])
        return Response({"status":"Access granted"})

    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        # if not request.user.is_creator:
        #     return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED) 
        project_name=request.GET.get('project_name')
        project=Project.objects.get(project_name=project_name)
        query=ProjectAccess.objects.filter(project_id=project)
        serializer=GetProjectAccessSerializer(query,many=True)
        return Response(serializer.data)
    
class AdminRemoveProjectAccess(APIView):
    def delete(self,request,pk):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_creator:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED) 
        projectAccess=ProjectAccess.objects.get(id=pk)
        project=projectAccess.project_id
        if not project.created_by==request.user:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED) 
        projectAccess.delete()
        return Response({"status":"Access revoked"})
    
    def put(self,request,pk):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_creator:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED) 
        projectAccess=ProjectAccess.objects.get(id=pk)
        project=projectAccess.project_id
        if not project.created_by==request.user:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED) 
        serializer=UpdateProjectAccessSerializer(projectAccess,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":"Access updated"})

class UserProjectDetailView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            project_name=request.GET.get('project_name')
            project=Project.objects.get(project_name=project_name)
            serializer=ProjectListSerializer(project)
            return Response(serializer.data)
        return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED) 
    
class UserProjectAccess(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_creator:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED) 
        username=request.GET.get('username')
        user=MyUser.objects.get(username=username)
        accesses=ProjectAccess.objects.filter(user_id=user)
        response=[]
        for access in accesses:
            response.append(access.project_id)
        serializer=ProjectListSerializer(response,many=True)
        return Response(serializer.data)

class ProjectRepositoryView(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        project_name=request.GET.get('project_name')
        project=Project.objects.get(project_name=project_name)
        try:
            projectAccess=ProjectAccess.objects.get(user_id=request.user,project_id=project)
        except:
            return Response({"error":"User not authorized"},status=status.HTTP_401_UNAUTHORIZED)
        repositoryList=Repository.objects.filter(project_id=project)
        serializer=RepositorySerializer(repositoryList,many=True)
        return Response(serializer.data)



        