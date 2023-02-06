from rest_framework import serializers
from api_services.models import Task, File, Comment, Account, Organization_Hierarchy


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task_id', 'assignor_name', 'assignor_email', 'assignee_name', 'assignee_email', 'title', 'description' ,'deadline', 'status']
        read_only_fields = ['task_id']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['task_id', 'file_address', 'file_name', 'file_type', 'uploaded_by_email']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['task_id', 'date_time', 'commentor_name', 'comment']


class Organization_HierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization_Hierarchy
        fields = ['user_role', 'priority', 'show_report']



class AccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name', 'last_name', 'user_role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            user_role = self.validated_data['user_role'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account