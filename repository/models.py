from django.db import models
from project.models import Project
from accounts.models import MyUser
# Create your models here.

class Repository(models.Model):
    project_id=models.ForeignKey(Project,on_delete=models.CASCADE)
    created_by=models.ForeignKey(MyUser, on_delete=models.SET_NULL)

class RepositoryContributor(models.Model):
    repo_id=models.ForeignKey(Repository, on_delete=models.CASCADE)
    user_id=models.ForeignKey(MyUser, on_delete=models.CASCADE)