from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.base import View
from django.utils import timezone
from .forms import TaskForm, SignUpForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class TaskListView(ListView):
    model = Task
    template_name = 'main_app_templates/task_list.html'
    context_object_name = 'task_list'
    queryset = Task.objects.filter(status=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = TaskForm()
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'main_app_templates/task_detail.html'
    context_object_name = 'task'


class TaskUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Task
    template_name = 'main_app_templates/task_action.html'
    context_object_name = 'task'
    form_class = TaskForm
    group_required = ('task_manager')
    


class TaskDeleteView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')
    context_object_name = 'task'
    template_name = 'main_app_templates/task_delete.html'
    group_required = ('task_manager')


class AddTask(LoginRequiredMixin, GroupRequiredMixin, View):
    group_required = ('task_manager')
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('task_list')


class CompeteTask(LoginRequiredMixin, View):
    def post(self, request, task_slug):
        task = get_object_or_404(Task, slug=task_slug)
        task.status = True
        task.completed = timezone.now()
        task.save()
        return redirect('task_list')


class LoginView(BaseLoginView):
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('task_list')
        return super().get(request, *args, **kwargs)


class RegisterCreateView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'
    success_message = 'You have successfully created an account. Now enter your username and password in the form below to log into your account.'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('task_list')
        return super().get(request, *args, **kwargs)