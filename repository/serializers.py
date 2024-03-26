from rest_framework import serializers
from .models import Repository,RepositoryContributor,Star_Repo
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

class AddContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model=RepositoryContributor
        fields="__all__"

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = MyUser
        fields = ["id","username","first_name","last_name","email","profile_pic","bio","dob"]

class GetContributorSerializer(serializers.ModelSerializer):
    user_id = MyUserSerializer()
    class Meta:
        model=RepositoryContributor
        fields="__all__"

class GetUserRepositorySerializer(serializers.ModelSerializer):
    stars=serializers.SerializerMethodField('get_stars_count')
    def get_stars_count(self,obj):
        count=Star_Repo.objects.filter(star_repo=obj).count()
        return count
    class Meta:
        model=Repository
        fields="__all__"

class StarRepoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Star_Repo
        fields="__all__"