from rest_framework import serializers
from .models import MyUser

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields = ('__all__')

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6)
        
