from django.urls import path
from .views import AdminProjectsCreateView,AdminProjectsUpdateView,UserProjectsListView,AdminProvideProjectAccess,AdminRemoveProjectAccess
urlpatterns = [
    path('adminProject',AdminProjectsCreateView.as_view()),
    path('adminProjectUpdate/<int:pk>',AdminProjectsUpdateView.as_view()),
    path('userProject',UserProjectsListView.as_view()),
    path('adminProjectAccess',AdminProvideProjectAccess.as_view()),
    path('adminProjectAccess/<int:pk>',AdminRemoveProjectAccess.as_view())
]
