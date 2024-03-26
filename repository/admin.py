from django.contrib import admin
from .models import Repository, RepositoryContributor,Star_Repo
# Register your models here.
admin.site.register(Repository)
admin.site.register(RepositoryContributor)
admin.site.register(Star_Repo)