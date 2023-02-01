import django_filters
from api_services.models import Task


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['assignor_email']