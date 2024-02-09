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
        print(attrs)
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        print(email,password)
        user = authenticate(email=email, password=password)
        print(user)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        print("Here")
        return {'email': user.email}
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)