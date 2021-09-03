from django.db import models
from django.db.models import fields
from rest_framework import serializers
from main.models import Task
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    completor = serializers.ReadOnlyField(source='completor.username')
    completed = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = '__all__'


class TaskCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('completor', 'completed', 'status')
        read_only_fields = ('completor', 'completed', 'status')


class UserSerializer(serializers.ModelSerializer):
    tasks_created = serializers.StringRelatedField(many=True)

    class Meta:
        model = User   
        fields = ('username', 'tasks_created')


