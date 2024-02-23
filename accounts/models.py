from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import project
# Create your models here.

class MyUser(AbstractUser):
    bio         = models.TextField(null=True, blank=True)
    dob         = models.DateField(null=True, blank=True)
    email       = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='images/',default='default.png') 
    is_creator  = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email
    
    @property
    def is_manager(self):
        query=self.users.filter(is_manager=True)
        if not query:
            return False
        else:
            return True   
    
    @property
    def current_project(self):
        projects=project.models.ProjectAccess.objects.filter(user_id=self).order_by('-created_at')
        if projects:
            return projects[0].project_id.project_name

    @receiver(post_save, sender = settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance = None, created = False, **kwargs):
        if created:
            token=Token.objects.create(user = instance)
