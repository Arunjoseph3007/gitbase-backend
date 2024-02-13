from django.urls import path
from .views import AdminProjectsCreateView,AdminProjectsUpdateView
urlpatterns = [
    path('adminProject',AdminProjectsCreateView.as_view()),
    path('adminProjectUpdate/<int:pk>',AdminProjectsUpdateView.as_view())
]
