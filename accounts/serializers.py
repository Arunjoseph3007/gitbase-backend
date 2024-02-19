from rest_framework import serializers
from .models import MyUser
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        exclude=('groups','user_permissions')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6)
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {'email': user.email}
        

class AdminListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['username','first_name','last_name','email','is_creator','is_manager','profile_pic','date_joined','current_project']