from django.urls import path
from .views import UserRepositoryView

urlpatterns = [
    path('userRepos',UserRepositoryView.as_view())
]