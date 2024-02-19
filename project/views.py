from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ProjectListSerializer,ProjectCreateSerializer
from .models import Project,ProjectAccess
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