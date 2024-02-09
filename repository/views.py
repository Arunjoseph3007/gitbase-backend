from django.shortcuts import render
from .serializers import RepositorySerializer
from .models import Repository,RepositoryContributor
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class AdminRepositoryView(APIView):
    def get(self,request):
        if request.user.is_creator:
            repositories=Repository.objects.all()
            serializer=RepositorySerializer(repositories,many=True)
            return Response(serializer.data)
        return Response({"error":"User not authorized"})

# class UserRepositoryView(APIView):
#     def get(self,request)