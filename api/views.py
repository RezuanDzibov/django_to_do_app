from django.utils import timezone
from main.models import Task
from . import serializers
from django.contrib.auth import get_user_model
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics


User = get_user_model()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name='Task manager').exists():
            serializer.save(creator=self.request.user)
        else:
            raise PermissionDenied({'detail': "You don't have permission to create task"})


class TaskCompleteView(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskCompleteSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(completor=self.request.user, status=True, completed=timezone.now())


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'

