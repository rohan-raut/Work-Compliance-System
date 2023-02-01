from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from api_services.models import Account, Task
import datetime
import requests
import json
from django.contrib.auth import logout

# Create your views here.

def dashboard_view(request):
    return render(request, 'dashboard.html')


def assign_task_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assignee_email = request.POST.get('assign_to')
        assignee_obj = Account.objects.get(email=assignee_email)
        assignee_name = assignee_obj.first_name + ' ' + assignee_obj.last_name
        deadline = request.POST.get('deadline')
        assignor_name = request.user.first_name + ' ' + request.user.last_name
        assignor_email = request.user.email
        status = "In Progress"

        task_obj = Task(assignor_name=assignor_name, assignor_email=assignor_email, assignee_name=assignee_name, assignee_email=assignee_email, title=title, description=description, deadline=deadline, status=status)

        task_obj.save()

        return redirect('/assigned-tasks')


    user_list = Account.objects.values()
    data = {}
    data['emails'] = []
    for x in user_list:
        data['emails'].append(x['email'])
        # data['first_name'].append(x['first_name'])
        # data['last_name'].append(x['last_name'])
    
    return render(request, 'assign_task.html', data)


def assigned_tasks_view(request):
    data = {}
    api = "http://127.0.0.1:8000/api/task-details?assignor_email=" + request.user.email
    resp = requests.get(api)
    json_data = json.loads(resp.text)
    data['task_list'] = json_data
    return render(request, 'assigned_tasks.html', data)


def to_do_view(request):
    return render(request, 'to_do.html')


def register_view(request):
    return render(request, 'register.html')


def login_view(request):
    if(request.method == "POST"):
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(request, email=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            return redirect('/login')
    else:
        return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('/login')
