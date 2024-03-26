from django.urls import path
from .views import UserRepositoryView,RepositoryDetailView,AddContributorView,ContributorDetailView,GetUserRepos,RepoSearch,StarRepoView,StarRepoDetail

urlpatterns = [
    path('userRepos',UserRepositoryView.as_view()),
    path('userRepos/<int:pk>',RepositoryDetailView.as_view()),
    path('contributor',AddContributorView.as_view()),
    path('contributor/<int:pk>',ContributorDetailView.as_view()),
    path('getUserRepos',GetUserRepos.as_view()),
    path('repoSearch',RepoSearch.as_view()),
    path('star-repo',StarRepoView.as_view()),
    path('star-repo-detail',StarRepoDetail.as_view()),
]