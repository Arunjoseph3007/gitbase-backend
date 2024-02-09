from django.urls import path
from .views import AdminProjectsView
urlpatterns = [
    path('adminProject',AdminProjectsView.as_view())
]
