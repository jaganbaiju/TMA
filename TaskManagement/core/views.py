from django.shortcuts import render
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . serializers import UserSerializer, UserResponseSerializer, TaskSerializer, TaskCompleteSerializer, TaskReportSerializer, UserUpdateSeriallizer
from . models import User, TaskModel
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken


# user register
@api_view(['POST'])
def user_register(request):
    username = request.data.get('username')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    role = request.data.get('role')
    password = request.data.get('password')


    if User.objects.filter(username=username).exists():
        return Response({
            "error": "username already exist"
        }, status=status.HTTP_409_CONFLICT)
    elif User.objects.filter(email=email).exists():
        return Response({
            "error": "email already exist"
        }, status=status.HTTP_409_CONFLICT)
    else:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
            password=password
        )

        return Response({
            "message": "user created successfully"
        }, status=status.HTTP_201_CREATED)
    

# all users
@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all().filter(role="user")
    admins = User.objects.all().filter(role="admin")
    
    serializer_users = UserResponseSerializer(users, many=True)
    serializer_admins = UserResponseSerializer(admins, many=True)

    return Response({
        "users": serializer_users.data,
        "admins": serializer_admins.data
    },
    status=status.HTTP_200_OK)


# login
@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = auth.authenticate(
        username=username,
        password=password
    )

    if user is None:
        return Response({
            "error": "Invalid Credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    return Response({
        "message": "Login Success",
        "access": str(access),
        "refresh": str(refresh)
    }, status=status.HTTP_200_OK)


# User Protected view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):

    user = request.user
    serializer = UserResponseSerializer(user)

    return Response(
        {
            "data": serializer.data,
        },
        status=status.HTTP_200_OK
    )
        
# user update delete
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def user_update_delete(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({
            "error": "user not found"
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserResponseSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    
    if request.method == 'PUT':
        serializer = UserUpdateSeriallizer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "user data updated"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PATCH':
        role = request.data.get('role')

        if not role:
            return Response({
            "error": "role required"
        }, status=status.HTTP_400_BAD_REQUEST)

        user.role = role
        user.save()

        return Response({
            "message": "role changed"
        }, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        user.delete()

        return Response({
            "message": "user deleted"
        }, status=status.HTTP_200_OK)

    
    

# create task
@api_view(['POST'])
def assign_task(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                "message": "Task created successfully..!!"
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

# view all tasks
@api_view(['GET'])
def get_tasks(request):
    all_tasks = TaskModel.objects.all()
    serializer = TaskSerializer(all_tasks, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    try:
        task = TaskModel.objects.get(pk=pk)
    except TaskModel.DoesNotExist:
        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "updated successfully"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        task.delete()
        return Response(
            {"message": "deleted successfully"},
            status=status.HTTP_200_OK
        )


# task report
@api_view(['GET'])
def task_report(request, pk):
    try:
        task = TaskModel.objects.get(pk=pk, status="completed")
    except TaskModel.DoesNotExist:
        return Response(
            {"error": "Completed task not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TaskReportSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PATCH', 'PUT'])
def user_task_view(request, pk):

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        tasks = user.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        task_id = request.data.get('taskId')
        task_status = request.data.get('status')

        if not task_id or not task_status:
            return Response(
                {"error": "taskId and status are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            task = user.tasks.get(id=task_id)
        except TaskModel.DoesNotExist:
            return Response(
                {"error": "Task not found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )

        task.status = task_status
        task.save()

        return Response(
            {"message": "task status updated"},
            status=status.HTTP_200_OK
        )


@api_view(['PATCH'])
def complete_task(request, pk):
    task = TaskModel.objects.get(pk=pk)

    task.status = request.data.get('status')
    task.worked_hours = request.data.get('worked_hours')
    task.completion_report = request.data.get('completion_report')

    task.save()

    return Response({
        "message": "Task Completed"
    })


    
