"""
URL configuration for todolist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from tasks.views import (tasks_view, add_task_view,del_task_view,complete_task_view, UserCreateView, LoginUserView, GenericTaskView, GenericCreateTaskView, GenericUpdateTaskView, GenericDetailTaskView,GenericDeleteTaskView, GenericCompleteTaskView)
from django.contrib.auth.views import LogoutView

from tasks.apiviews import TaskListAPI, TaskViewSet

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('api/tasks', TaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', GenericTaskView.as_view()),
    path('tasksapi/', TaskListAPI.as_view()),
    path('add-task/', GenericCreateTaskView.as_view()), 
    path('update-task/<pk>', GenericUpdateTaskView.as_view()), 
    path('detail-task/<pk>', GenericDetailTaskView.as_view()), 
    path('del-task/<pk>',GenericDeleteTaskView.as_view()),
    path('user/signin/',UserCreateView.as_view()),
    path('user/login/',LoginUserView.as_view()),
    path('user/logout/', LogoutView.as_view()),
    path('complete-task/<pk>/', GenericCompleteTaskView.as_view()),
] + router.urls