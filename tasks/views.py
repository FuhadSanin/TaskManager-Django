from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from tasks.models import Tasks
from django.views import View

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

#Generic-based view

class AuthorisationTaskView(LoginRequiredMixin):
    def get_queryset(self):
        tasks = Tasks.objects.filter(status=False , user=self.request.user)
        return tasks


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = "/user/login"

class LoginUserView(LoginView):
    template_name = "user_login.html"

class GenericTaskView(AuthorisationTaskView, ListView):
    template_name = "index.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_queryset(self):
        search = self.request.GET.get('search', '').strip() 
        tasks = Tasks.objects.filter(user=self.request.user)

        if search:
            tasks = tasks.filter(title__icontains=search)

        return tasks

    def get_context_data(self, **kwargs):
        """
        Extend context to include filtered tasks and task status counts.
        """
        context = super().get_context_data(**kwargs)

        # Use a single query to fetch all tasks and split results in-memory
        all_tasks = self.get_queryset()
        pending_tasks = all_tasks.filter(status=False)
        completed_tasks = all_tasks.filter(status=True)

        context.update({
            "all": all_tasks,  # Tasks already paginated
            "pending": pending_tasks,  # Pending tasks
            "completed": completed_tasks,  # Completed tasks
        })

        return context
    
class GenericCreateTaskView(AuthorisationTaskView,CreateView):
    model = Tasks
    template_name = "task_create.html"
    fields = ("title", "description")
    success_url = "/tasks"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    
class GenericUpdateTaskView(AuthorisationTaskView,UpdateView):
    model = Tasks
    template_name = "task_update.html"
    fields = ("title", "description")
    success_url = "/tasks"

class GenericDetailTaskView(AuthorisationTaskView,DetailView):
    model = Tasks
    template_name = "task_detail.html"

class GenericDeleteTaskView(AuthorisationTaskView,DeleteView):
    model = Tasks
    template_name = "task_delete.html"
    success_url = "/tasks"

class GenericCompleteTaskView(AuthorisationTaskView,UpdateView):
    model = Tasks
    template_name = "task_complete.html"
    fields = ("status",)
    success_url = "/tasks"



#Class-based view
class TaskView(View):
    def get(self,request):
        search = request.GET.get('search')
        tasks = Tasks.objects.filter(status=False)
        completed = Tasks.objects.filter(status=True)

        if search:
            tasks = tasks.filter(title__icontains=search)
        return render(request, 'index.html', {
            'tasks': tasks,
            'completed': completed
        })


#Fuction-based view
def tasks_view(request):
    search = request.GET.get('search')
    tasks = Tasks.objects.filter(status=False)
    completed = Tasks.objects.filter(status=True)

    if search:
        tasks = tasks.filter(title__icontains=search)
    return render(request, 'index.html', {
        'tasks': tasks,
        'completed': completed
    })

def add_task_view(request):
    task = request.GET.get('task')
    Tasks(title=task).save()
    return HttpResponseRedirect('/tasks')

def del_task_view(request,index):
    Tasks.objects.filter(id=index).delete()
    return HttpResponseRedirect('/tasks')

def complete_task_view(request,index):
    Tasks.objects.filter(id=index).update(status=True)
    return HttpResponseRedirect('/tasks')
