from django.urls import path
from api_services.views import task_list, task_detail



urlpatterns = [
    path('task-details/', task_list, name="task_list"),
    path('task-details/<int:pk>/', task_detail, name="task_detail"),
]

