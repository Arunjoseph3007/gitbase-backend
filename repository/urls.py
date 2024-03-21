from django.urls import path
from .views import UserRepositoryView,RepositoryDetailView

urlpatterns = [
    path('userRepos',UserRepositoryView.as_view()),
    path('userRepos/<int:pk>',RepositoryDetailView.as_view()),
]