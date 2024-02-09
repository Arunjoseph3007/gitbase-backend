from django.contrib import admin
from .models import Repository, RepositoryContributor
# Register your models here.
admin.site.register(Repository)
admin.site.register(RepositoryContributor)