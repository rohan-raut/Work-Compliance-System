from django.urls import path
from web_app.views import dashboard_view, assign_task_view, assigned_tasks_view, to_do_view, register_view, login_view, logout_view, make_hierarchy_view



urlpatterns = [
    path('dashboard/', dashboard_view, name="dashboard_view"),
    path('assign-task/', assign_task_view, name="assign_task_view"),
    path('assigned-tasks/', assigned_tasks_view, name="assigned_tasks_view"),
    path('to-do/', to_do_view, name="to_do_view"),
    path('register/', register_view, name="register_view"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('make-hierarchy/', make_hierarchy_view, name="make_hierarchy_view"),
]

