from django.shortcuts import render
from .serializers import RepositorySerializer
from .models import Repository,RepositoryContributor
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class UserRepositoryView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            repos=[]
            contributors=RepositoryContributor.objects.filter(user_id=request.user)
            for contributor in contributors:
                repos.append(Repository.objects.get(id=contributor.repo_id.id))
            serializer=RepositorySerializer(repos,many=True)
            return Response(serializer.data)
        return Response({"error":"User not authorized"})
