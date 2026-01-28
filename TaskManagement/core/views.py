from django.shortcuts import render
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . serializers import UserSerializer, UserResponseSerializer, TaskSerializer, TaskCompleteSerializer, TaskReportSerializer, UserUpdateSeriallizer
from . models import User, TaskModel
from rest_framework.permissions import IsAuthenticated



# user register view
class UserAPIVew(APIView):

    permission_classes = []

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "User created successfully..!!"
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def get(self, request):
        all_users = User.objects.all().filter(role="user")
        serializer_users = UserResponseSerializer(all_users, many=True)

        all_admins = User.objects.all().filter(role="admin")
        serializer_admins = UserResponseSerializer(all_admins, many=True)

        return Response({
            "users": serializer_users.data,
            "admins": serializer_admins.data
        },
        status=status.HTTP_200_OK)


        

# user dashboard
class UserProtectedView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        serializer = UserResponseSerializer(user)

        return Response(
            {
                "message": "Login Successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )
    

class UserUpdateDelView(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserUpdateSeriallizer(user, data=request.data)
        

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "data updated"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        user = self.get_object(pk)
        role = request.data['role']

        user.role = role
        user.save()

        return Response({
            "message": "role changed"
        })
    
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response({
            "message": "deleted successfully"
        })
    

# create task
class TaskAPIView(APIView):

    def get(self, request):
        all_tasks = TaskModel.objects.all()
        serializer = TaskSerializer(all_tasks, many=True)

        return Response(serializer.data)

    def post(self, request):
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
    

class TaskDetailView(APIView):
    def get_object(self, pk):
        try:
            return TaskModel.objects.get(pk=pk)
        except TaskModel.DoesNotExist:
            raise Http404
        
    
    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)

        return Response(serializer.data)
    

    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "updated successfully"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response({
            "message": "deleted successfully"
        })



class TaskReportView(APIView):
    def get(self, request, pk):
        task = TaskModel.objects.get(pk=pk, status="completed")
        if not task:
            raise Http404
        
        serializer = TaskReportSerializer(task)
        return Response(serializer.data)
        

class UserTaskView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        user = self.get_object(pk)

        tasks = user.tasks.all()
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        user = self.get_object(pk)
        task_id = request.data['taskId']
        task_status = request.data['status']

        task = user.tasks.get(id=task_id)

        task.status = task_status
        task.save()

        return Response({
            "message": f"task in process"
        })


    def put(self, request, pk):
        # user = self.get_object(pk)
        # task_id = request.data['taskId']
        task = TaskModel.objects.get(pk=pk)

        serializer = TaskCompleteSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "task completed"
            })
