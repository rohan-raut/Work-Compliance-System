from django.urls import path
from web_app.views import dashboard_view, assign_task_view, assigned_tasks_view, to_do_view, register_view, login_view, logout_view, make_hierarchy_view, task_detail_view, profile_view, error_view, all_users_view, delete_user_view, change_task_status, add_comment, send_reminder_cronjob, change_status_cronjob, update_task_details_view



urlpatterns = [
    path('dashboard/', dashboard_view, name="dashboard_view"),
    path('assign-task/', assign_task_view, name="assign_task_view"),
    path('assigned-tasks/', assigned_tasks_view, name="assigned_tasks_view"),
    path('task-detail/<int:pk>/', task_detail_view, name="task_detail_view"),
    path('update-task-details/<int:pk>/', update_task_details_view, name="update_task_details_view"),
    path('to-do/', to_do_view, name="to_do_view"),
    path('register/', register_view, name="register_view"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('make-hierarchy/', make_hierarchy_view, name="make_hierarchy_view"),
    path('profile/<str:pk>/', profile_view, name="profile_view"),
    path('error/', error_view, name="error_view"),
    path('all-users/', all_users_view, name="all_users_view"),
    path('delete/<str:pk>/', delete_user_view, name="delete_user_view"),
    path('change-task-status/<str:pk>/', change_task_status, name="change_task_status"),
    path('add-comment/<str:pk>/', add_comment, name="add_comment"),
    path('send-reminder-cronjob/', send_reminder_cronjob, name="send_reminder_cronjob"),
    path('change-status-cronjob/', change_status_cronjob, name="change_status_cronjob"),
]

