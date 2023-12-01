from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    bio         = models.TextField(null=True, blank=True)
    dob         = models.DateField(null=True, blank=True)
    email       = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='images/',null=True,blank=True) 
    is_creator  = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.username

