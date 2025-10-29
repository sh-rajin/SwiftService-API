from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name', 'email')
        
    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Username is already taken.'})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email is already registered.'})
        
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        
        user.set_password(password)
        user.is_active = False
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
        
        