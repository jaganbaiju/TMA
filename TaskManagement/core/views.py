from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . serializers import UserSerializer
from . models import User
from rest_framework.permissions import IsAuthenticated


# user register view
class UserRegisterAPIVew(APIView):

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
        

# user dashboard
class UserProtectedView(APIView):

    permission_classes = [IsAuthenticated,]

    def get(self, request):

        return Response(
            {
                "message": "authenticated..",
                "user": request.data.username
            }
        )