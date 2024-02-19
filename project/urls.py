from django.urls import path
from .views import AdminProjectsCreateView,AdminProjectsUpdateView,UserProjectsListView
urlpatterns = [
    path('adminProject',AdminProjectsCreateView.as_view()),
    path('adminProjectUpdate/<int:pk>',AdminProjectsUpdateView.as_view()),
    path('userProject',UserProjectsListView.as_view())
]
