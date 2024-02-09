from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ProjectSerializer
from .models import Project
from rest_framework.response import Response
# Create your views here.
class AdminProjectsView(APIView):
    def get(self,request):
        if request.user.is_creator:
            projects=Project.objects.all()
            serializer=ProjectSerializer(projects,many=True)
            return Response(serializer.data)
        return Response({"error":"User not authorized"})
