from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from api_services.models import Account, Task, Organization_Hierarchy
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
    data = {}
    hierarchy = Organization_Hierarchy.objects.all()
    data['user_roles'] = hierarchy
    return render(request, 'register.html', data)


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


def make_hierarchy_view(request):

    if(request.method == "POST"):
        data_list = []
        for key in request.POST.items():
            lst = key[0].split('_')
            if(lst[0] == 'user' and request.POST[key[0]] != ''):  # checking for blank data row
                data_list.append({
                    'user_role': request.POST[key[0]],
                    'priority': request.POST['priority_' + lst[2]],
                    'show_report': request.POST['show_report_' + lst[2]],
                    })
        
        # delete all present rows and add new data
        Organization_Hierarchy.objects.all().delete()
        for x in data_list:
            show_report_in_bool = True
            if(x['show_report'] == 'N'):
                show_report_in_bool = False
            obj = Organization_Hierarchy(user_role=x['user_role'], priority=x['priority'], show_report=show_report_in_bool)
            obj.save()

        

    data = {}
    api = "http://127.0.0.1:8000/api/organization-hierarchy/"
    resp = requests.get(api)
    data['objs'] = json.loads(resp.text)

    counter = 0
    for x in data['objs']:
        x['num'] = counter
        counter = counter + 1
    
    data['rows'] = len(data['objs'])
    
    return render(request, 'make_hierarchy.html', data)



def task_detail_view(request, pk):
    data = {}
    api = "http://127.0.0.1:8000/api/task-details/" + str(pk) + "/"
    resp = requests.get(api)
    json_data = json.loads(resp.text)
    data = json_data
    print(data)
    return render(request, 'task_detail.html', data)    






# git remote add origin git@github.com:rohan-raut/Work-Compliance-System.git
# git branch -M main
# git push -u origin main