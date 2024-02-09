from rest_framework import serializers
from .models import Project,ProjectAccess
from repository.models import Repository

class ProjectSerializer(serializers.ModelSerializer):
    members_count=serializers.SerializerMethodField('get_members_count')
    def get_members_count(self,obj):
        count=ProjectAccess.objects.filter(project_id=obj.id).count()
        return count
    repos_count=serializers.SerializerMethodField('get_repos_count')
    def get_repos_count(self,obj):
        count=Repository.objects.fiter(project_id=obj.id).count()
        return count
    class Meta:
        model=Project
        fields=['project_name','project_description','created_at','members_count','repos_count']