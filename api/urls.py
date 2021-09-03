from django.urls import path
from django.urls.conf import include, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('tasks', views.TaskViewSet)
router.register('users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('task_complete/<slug:slug>/', views.TaskCompleteView.as_view())
]
