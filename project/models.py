from django.db import models
from accounts.models import MyUser
# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(MyUser,on_delete=models.SET_NULL)
    project_description = models.TextField(blank=True,null=True)

class ProjectAccess(models.Model):
    project_id=models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    # role=models.CharField(max_length=200)
