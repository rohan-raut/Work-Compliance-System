from rest_framework import serializers
from api_services.models import Tasks, Files, Comments


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['task_id', 'assignor_name', 'assignor_email', 'assignee_name', 'assignee_email', 'title', 'description' ,'deadline', 'status']


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['task_id', 'file_address', 'file_name', 'file_type', 'uploaded_by_email']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['task_id', 'date_time', 'commentor_name', 'comment']
