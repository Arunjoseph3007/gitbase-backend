from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ProjectListSerializer,ProjectCreateSerializer,ProjectAccessSerializer
from .models import Project,ProjectAccess
from accounts.models import MyUser
from rest_framework.response import Response
# Create your views here.
class AdminProjectsCreateView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_creator:
                projects=Project.objects.all()
                serializer=ProjectListSerializer(projects,many=True)
                return Response(serializer.data)
        return Response({"error":"User not authorized"})

    def post(self,request):
        if request.user.is_authenticated:
            if request.user.is_creator:
                user=request.user
                serializer=ProjectCreateSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(created_by=user)
                return Response(serializer.data)
        return Response({"error":"User not authorized"})

class AdminProjectsUpdateView(APIView):
    def put(self,request,pk):
        if request.user.is_authenticated:
            if request.user.is_creator:
                project_description=request.POST.get('project_description')
                project=Project.objects.get(id=pk)
                project.project_description=project_description
                project.save()
                serializer=ProjectCreateSerializer(project)
                return Response(serializer.data)
        return Response({"error":"User not authorized"})    
    
    def delete(self,request,pk):
        if request.user.is_authenticated:
            if request.user.is_creator:
                Project.objects.get(id=pk).delete()   
                return Response({"status":"Project deleted"})
        return Response({"error":"User not authorized"}) 

class UserProjectsListView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            projects=[]
            projectAccess=ProjectAccess.objects.filter(user_id=request.user)
            for project in projectAccess:
                projects.append(Project.objects.get(id=project.project_id.id))
            serializer=ProjectListSerializer(projects,many=True)
            return Response(serializer.data)
        return Response({"error":"User not authorized"})

class AdminProvideProjectAccess(APIView):
    def post(self,request):
        if request.user.is_authenticated:
            if request.user.is_creator:
                user_id=request.POST.get('user_id')
                project_id=request.POST.get('project_id')
                is_manager=request.POST.get('is_manager')
                user=MyUser.objects.get(id=user_id)
                project=Project.objects.get(id=project_id)
                if is_manager=="True":
                    ProjectAccess.objects.create(user_id=user,project_id=project,is_manager=True)
                else:
                    ProjectAccess.objects.create(user_id=user,project_id=project)
                return Response({"status":"Access provided"})
        return Response({"error":"User not authorized"})

    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_creator:
                project_name=request.GET.get('project_name')
                project=Project.objects.get(project_name=project_name)
                query=ProjectAccess.objects.filter(project_id=project)
                serializer=ProjectAccessSerializer(query,many=True)
                return Response(serializer.data)
        return Response({"error":"User not authorized"})


    
    
class AdminRemoveProjectAccess(APIView):
    def delete(self,request,pk):
        if request.user.is_authenticated:
            if request.user.is_creator:
                ProjectAccess.objects.get(id=pk).delete()
                return Response({"status":"Access revoked"})
        return Response({"error":"User not authorized"})
    
    def put(self,request,pk):
        if request.user.is_authenticated:
            if request.user.is_creator:
                is_manager=request.POST.get('is_manager')
                access=ProjectAccess.objects.get(id=pk)
                if is_manager=="True":
                    access.is_manager=True
                else:
                    access.is_manager=False
                return Response({"status":"Access updated"})
        return Response({"error":"User not authorized"})