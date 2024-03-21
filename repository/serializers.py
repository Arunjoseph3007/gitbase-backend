from rest_framework import serializers
from .models import Repository,RepositoryContributor
from accounts.models import MyUser
from project.models import Project

class RepositoryCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['id','username','profile_pic']

class ProjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['project_name']

class RepositorySerializer(serializers.ModelSerializer):
    created_by=RepositoryCreatorSerializer()
    project_id=ProjectNameSerializer()
    contributors_count=serializers.SerializerMethodField('get_contributors_count')
    def get_contributors_count(self,obj):
        count=RepositoryContributor.objects.filter(repo_id=obj.id).count()
        return count
    class Meta:
        model=Repository
        fields="__all__"

class RepositoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Repository
        fields=("repo_name","repo_description","project_id")

