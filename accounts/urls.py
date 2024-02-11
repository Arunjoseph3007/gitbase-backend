from django.urls import path,include
from .views import RegistrationView,LoginView,ChangePasswordView

urlpatterns = [
    path('register',RegistrationView.as_view()),
    path('login',LoginView.as_view()),
    path('change_password',ChangePasswordView.as_view(),name='passwordChange'),
    # path('password_reset_email',ChangePasswordEmailView.as_view()),
    # path('verifyEmail',verifyEmail.as_view(),name='verifyEmail')
]
