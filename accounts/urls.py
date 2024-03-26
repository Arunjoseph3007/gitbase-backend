from django.urls import path,include
from .views import RegistrationView,LoginView,ChangePasswordView,UserSearchView,MyUserView

urlpatterns = [
    path('register',RegistrationView.as_view()),
    path('login',LoginView.as_view()),
    path('change_password',ChangePasswordView.as_view(),name='passwordChange'),
    path('userSearch',UserSearchView.as_view()),
    path('MyUser',MyUserView.as_view())
]
