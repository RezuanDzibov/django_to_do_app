from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('task_detail/<slug:slug>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task_edit/<slug:slug>/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('task_delete/<slug:slug>/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task_add/', views.AddTask.as_view(), name='task_add'),
    path('task_complete/<slug:task_slug>/', views.CompeteTask.as_view(), name='task_complete')
]