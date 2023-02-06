import django_filters
from api_services.models import Task, Organization_Hierarchy


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['assignor_email']


class Organization_Hierarchy_Filter(django_filters.FilterSet):
    class Meta:
        model = Organization_Hierarchy
        fields = ['user_role', 'priority', 'show_report']