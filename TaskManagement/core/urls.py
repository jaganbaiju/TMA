from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('user-register/', views.user_register),
    path('all-user/', views.get_all_users),
    path('login/', views.user_login),

    path('token/refresh/', TokenRefreshView.as_view()),


    path('user-dash/', views.user_dashboard),
    path('user-del-upd/<int:pk>/', views.user_update_delete),
    
    path('create-task/', views.assign_task),
    path('tasks/', views.get_tasks),

    path('tasks/<int:pk>/', views.task_detail),
    path('tasks/<int:pk>/report/', views.task_report),
    path('usr-all-task/<int:pk>/', views.user_task_view),
]
