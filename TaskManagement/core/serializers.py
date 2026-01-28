from rest_framework import serializers
from . models import User, TaskModel


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


class UserUpdateSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['id', 'title', 'description', 'assigned_to', 'due_date', 'status']


class TaskCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['status', 'completion_report', 'worked_hours']


class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['id', 'title', 'status', 'completion_report', 'worked_hours']