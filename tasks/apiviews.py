from django.views import View
from django.http.response import JsonResponse

from tasks.models import Tasks
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","username","password"]

class TaskSerializer(ModelSerializer):
    user = UserSerializer(read_only = True) # no editing option
    class Meta:
        model = Tasks
        fields = ["id","title", "description", "status","user"]

class TaskViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

class TaskListAPI(APIView):
    def get(self,request):
        tasks = Tasks.objects.all()
        # data = []
        # for task in tasks:
        #     data.append({"title" : task.title})
        data = TaskSerializer(tasks,many=True).data #it is used to convert model into json
        return Response({"tasks" :data})
