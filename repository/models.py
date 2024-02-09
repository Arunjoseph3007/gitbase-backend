from django.db import models
from project.models import Project
from accounts.models import MyUser
# Create your models here.

class Repository(models.Model):
    repo_name=models.CharField(max_length=200,null=True,blank=True)
    project_id=models.ForeignKey(Project,on_delete=models.CASCADE)
    created_by=models.ForeignKey(MyUser, on_delete=models.SET_NULL,blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.repo_name)

class RepositoryContributor(models.Model):
    repo_id=models.ForeignKey(Repository, on_delete=models.CASCADE)
    user_id=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.repo_id)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'repo_id'], name='user_id&repo_id'
            )
        ]