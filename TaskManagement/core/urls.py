from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('user-api/', views.UserAPIVew.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('user-dash/', views.UserProtectedView.as_view()),
    path('user-del-upd/<int:pk>/', views.UserUpdateDelView.as_view()),
    
    path('tasks/', views.TaskAPIView.as_view()),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view()),
    path('tasks/<int:pk>/report/', views.TaskReportView.as_view()),
    path('usr-all-task/<int:pk>/', views.UserTaskView.as_view())
]
