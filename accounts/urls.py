from django.urls import path,include
from .views import RegistrationView,LoginView,ChangePasswordView,ChangePasswordEmailView

urlpatterns = [
    path('register',RegistrationView.as_view()),
    path('login',LoginView.as_view()),
    path('change_password',ChangePasswordView.as_view()),
    path('password_reset_email',ChangePasswordEmailView.as_view())
]
