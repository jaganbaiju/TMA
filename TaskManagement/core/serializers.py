from rest_framework import serializers
from . models import User


# serializer for user
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'password']

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            role=validated_data['role'],
            password=validated_data['password']
        )

        return user
    

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'