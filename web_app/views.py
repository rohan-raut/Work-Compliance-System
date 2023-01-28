from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.

def dashboard_view(request):
    return render(request, 'dashboard.html')


def assign_task_view(request):
    return render(request, 'assign_task.html')


def assigned_tasks_view(request):
    return render(request, 'assigned_tasks.html')


def to_do_view(request):
    return render(request, 'to_do.html')


def register_view(request):
    return render(request, 'register.html')


def login_view(request):
    return render(request, 'login.html')
