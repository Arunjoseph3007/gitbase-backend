from django.urls import path
from .views import AdminProjectsCreateView,AdminProjectsUpdateView,UserProjectsListView,UserProjectDetailView,AdminProvideProjectAccess,AdminRemoveProjectAccess,UserProjectAccess
urlpatterns = [
    path('',UserProjectAccess.as_view()),
    path('adminProject',AdminProjectsCreateView.as_view()),
    path('adminProjectUpdate/<int:pk>',AdminProjectsUpdateView.as_view()),
    path('userProject',UserProjectsListView.as_view()),
    path('userProjectDetail',UserProjectDetailView.as_view()),
    path('adminProjectAccess',AdminProvideProjectAccess.as_view()),
    path('adminProjectAccess/<int:pk>',AdminRemoveProjectAccess.as_view())
]
