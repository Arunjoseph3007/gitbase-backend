from rest_framework import serializers
from .models import Project,ProjectAccess
from repository.models import Repository
from accounts.models import MyUser

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['id','username','profile_pic','first_name','last_name','email']

class ProjectListSerializer(serializers.ModelSerializer):
    members_count=serializers.SerializerMethodField('get_members_count')
    def get_members_count(self,obj):
        count=ProjectAccess.objects.filter(project_id=obj.id).count()
        return count
    repos_count=serializers.SerializerMethodField('get_repos_count')
    def get_repos_count(self,obj):
        count=Repository.objects.filter(project_id=obj.id).count()
        return count
    created_by=UserDetailSerializer()
    class Meta:
        model=Project
        fields=['id','project_name','project_description','created_at','members_count','repos_count','created_by']

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id','project_name','project_description']

class GetProjectAccessSerializer(serializers.ModelSerializer):
    user_id=UserDetailSerializer()
    class Meta:
        model=ProjectAccess
        fields="__all__"

class PostProjectAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProjectAccess
        fields="__all__"

class UpdateProjectAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProjectAccess
        fields=("is_manager",)