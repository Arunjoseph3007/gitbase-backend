from django.db import models
from accounts.models import MyUser
from django.utils import timezone
# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=200,unique=True)
    created_by = models.ForeignKey(MyUser,on_delete=models.SET_NULL,blank=True, null=True)
    project_description = models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.project_name

class ProjectAccess(models.Model):
    project_id=models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id=models.ForeignKey(MyUser, on_delete=models.CASCADE,related_name='users')
    is_manager=models.BooleanField(default=False)
    created_at=models.DateTimeField( default=timezone.now)
    def __str__(self):
        return (f"{self.project_id.project_name} {self.user_id.username}")
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'project_id'], name='user_id&project_id'
            )
        ]