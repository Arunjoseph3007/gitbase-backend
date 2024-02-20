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
            project_name=request.POST.get('project_name')
            project=Project.objects.get(project_name=project_name)
            print(request.user)
            try:
                query=ProjectAccess.objects.get(is_manager=True,project_id=project,user_id=request.user)
            except:
                return Response({"error":"User not authorized"})
            user_id=request.POST.get('user_id')
            is_manager=request.POST.get('is_manager')
            user=MyUser.objects.get(id=user_id)
            if is_manager=="True":
                ProjectAccess.objects.create(user_id=user,project_id=project,is_manager=True)
            else:
                ProjectAccess.objects.create(user_id=user,project_id=project)
            return Response({"status":"Access granted"})
        return Response({"error":"User not authorized"})

    def get(self,request):
        if request.user.is_authenticated:
            project_name=request.GET.get('project_name')
            try:
                project=Project.objects.get(project_name=project_name)
            except:
                return Response({"error":"Project not found"})
            query=ProjectAccess.objects.filter(project_id=project)
            serializer=ProjectAccessSerializer(query,many=True)
            return Response(serializer.data)
        return Response({"error":"User not authorized"})
    
class AdminRemoveProjectAccess(APIView):
    def delete(self,request,pk):
        if request.user.is_authenticated:
            try:
                projectAccess=ProjectAccess.objects.get(id=pk)
                project=ProjectAccess.objects.get(project_id=projectAccess.project_id,user_id=request.user,is_manager=True)
            except:
                return Response({"error":"Project not found"})
            projectAccess.delete()
            return Response({"status":"Access revoked"})
        return Response({"error":"User not authorized"})
    
    def put(self,request,pk):
        if request.user.is_authenticated:
            try:
                projectAccess=ProjectAccess.objects.get(id=pk)
                project=ProjectAccess.objects.get(project_id=projectAccess.project_id,user_id=request.user,is_manager=True)
            except:
                return Response({"error":"Project not found"})
            is_manager=request.POST.get('is_manager')
            if is_manager=="True":
                projectAccess.is_manager=True
            else:
                projectAccess.is_manager=False
            projectAccess.save()
            return Response({"status":"Access updated"})
        return Response({"error":"User not authorized"})
    
class UserProjectDetailView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            project_name=request.GET.get('project_name')
            try:
                project=Project.objects.get(project_name=project_name)
            except:
                return Response({"status":"Project not found"})
            serializer=ProjectListSerializer(project)
            return Response(serializer.data)
        return Response({"error":"User not authorized"}) 