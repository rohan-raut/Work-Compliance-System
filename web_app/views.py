from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from api_services.models import Account, Task, Organization_Hierarchy, File, Comment
import datetime
import requests
import json
from django.contrib.auth import logout

# importing for notification
import smtplib, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# global variable declaration and assignment
global sender_email, sender_name, password, hostname, port

sender_email = "rohan.raut@mmit.edu.in"
sender_name = "no reply"
password = "chzhpfltnmgwnfnv"
hostname = "127.0.0.1"
port = "8000"


# fuction to send email notification
def send_notification(receiver_email, subject, body):
    try:
        smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=587)
        smtpObj.starttls()
        smtpObj.login(sender_email, password)
        message = MIMEMultipart()
        message["From"] = sender_name
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        text = message.as_string()
        smtpObj.sendmail(sender_email, receiver_email, text)
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")



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
        files = request.FILES.getlist('upload_file')

        task_obj = Task(assignor_name=assignor_name, assignor_email=assignor_email, assignee_name=assignee_name, assignee_email=assignee_email, title=title, description=description, deadline=deadline, status=status)
        task_obj.save()

        last_obj = Task.objects.last()
        task_id = last_obj.task_id     

        email_subject = "New Task: " + title
        email_body = "Hi {},\n{} assigned a new task which is due on {}.\nLink to the Task: http://{}:{}/task-detail/{}/".format(assignee_name, assignor_name, deadline, hostname, port, task_id) 
        send_notification(assignee_email, email_subject, email_body)

        for x in files:
            file_obj = File(task_id=task_id, file=x, uploaded_by_email=assignor_email)
            file_obj.save()

        return redirect('/assigned-tasks')


    user_list = Account.objects.values()
    hierarchy = Organization_Hierarchy.objects.all()
    data = {}
    data['user_info'] = []

    hierarchy_map = {}
    for x in hierarchy:
        hierarchy_map[x.user_role] = x.priority


    for x in user_list:
        if(hierarchy_map[x['user_role']] >= hierarchy_map[request.user.user_role] and x['email'] != request.user.email):
            data['user_info'].append({'email': x['email'], 'name': x['first_name']+' '+x['last_name']})
    
    return render(request, 'assign_task.html', data)


def assigned_tasks_view(request):
    data = {}
    api = "http://127.0.0.1:8000/api/task-details?assignor_email=" + request.user.email
    resp = requests.get(api)
    json_data = json.loads(resp.text)
    data['task_list'] = json_data

    # Convert datatime to date
    for x in data['task_list']:
        x['deadline'] = x['deadline'][0:10]
    return render(request, 'assigned_tasks.html', data)


def to_do_view(request):
    data = {}
    api = "http://127.0.0.1:8000/api/task-details?assignee_email=" + request.user.email + "&status=In Progress"
    resp = requests.get(api)
    json_data = json.loads(resp.text)
    data['task_list'] = json_data

    # Convert datatime to date
    for x in data['task_list']:
        x['deadline'] = x['deadline'][0:10]
    return render(request, 'to_do.html', data)


def register_view(request):
    if(request.method == 'POST'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        department = request.POST['department']
        user_role = request.POST['user_role']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if(password1 == password2):
            new_user = Account(email=email, username=email, first_name=first_name, last_name=last_name, user_role=user_role, department=department, phone=phone)
            new_user.set_password(password1)
            new_user.save()
        else:
            return HttpResponse("<p>Password's should match.</p>")

    data = {}
    hierarchy = Organization_Hierarchy.objects.all()
    data['user_roles'] = hierarchy
    return render(request, 'register.html', data)


def login_view(request):
    if(request.method == "POST"):
        username = request.POST.get('email')
        password = request.POST.get('password')
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
    if request.method == "POST":
        files = request.FILES.getlist('upload_file')
        for x in files:
            file_obj = File(task_id=pk, file=x, uploaded_by_email=request.user.email)
            file_obj.save()
        task = Task.objects.get(task_id=pk)
        task.status = "Under Review"
        task.save()
        email_subject = "Task Submitted: " + task.title
        email_body = "Hi {},\n{} just completed the task - {}, please make sure to review the submitted task and update the status.\nLink to the task: http://{}:{}/task-detail/{}/".format(task.assignor_name, task.assignee_name, task.title, hostname, port, pk)
        send_notification(task.assignor_email, email_subject, email_body)

    data = {}
    data['task_details'] = Task.objects.get(task_id=pk)
    data['files'] = File.objects.filter(task_id=pk)
    data['file_cnt'] = len(File.objects.filter(task_id=pk, uploaded_by_email=data['task_details'].assignee_email))
    data['comments'] = Comment.objects.filter(task_id=pk)
    return render(request, 'task_detail.html', data)    



def profile_view(request, pk):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        department = request.POST['department']
        user_role = request.POST['user_role']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        user = Account.objects.get(email=pk)
        if first_name != '':
            user.first_name = first_name
        if last_name != '':
            user.last_name = last_name
        if phone != '':
            user.phone = phone
        user.department = department
        user.user_role = user_role

        if old_password != '':
            check_user = authenticate(request, email=request.user.email, password=old_password)
            if check_user is not None:
                user.set_password(new_password)
            else:
                # throw an error
                print("Old password does not match")
        user.save()

    data = {}
    if (request.user.is_superuser == False and pk != request.user.email):
        data['message'] = "You do not have access to this information"
        return render(request, 'error.html', data)

    user = Account.objects.get(email=pk)
    data['user_detail'] = user
    hierarchy = Organization_Hierarchy.objects.all()
    data['user_roles'] = hierarchy
    return render(request, 'profile.html', data)


def error_view(request):
    return render(request, 'error.html')


def all_users_view(request):
    data = {}
    data['users'] = Account.objects.all()
    return render(request, 'all_users.html', data)


def delete_user_view(request, pk):
    user = Account.objects.get(email=pk)
    user.delete()
    return redirect('/all-users')


def change_task_status(request, pk):
    task = Task.objects.get(task_id=pk)
    status = request.POST['change_status']
    task.status = status
    task.save()
    
    email_subject = "Task Status: " + task.title
    if status == "In Progress":
        email_body = "Hi {},\n{} just reviewed your task - {} and your task has not been approved. Please make the necessary changes and resubmit it before the due date.\nLink to task page: http://{}:{}/task-detail/{}/".format(task.assignee_name, task.assignor_name, task.title, hostname, port, task.task_id)
        send_notification(task.assignee_email, email_subject, email_body)
    else:
        email_body = "Hi {},\n{} just reviewed your task - {} and your task has been approved. You can check the status of your task using the below link.\nLink to task page: http://{}:{}/task-detail/{}/".format(task.assignee_name, task.assignor_name, task.title, hostname, port, task.task_id)
        send_notification(task.assignee_email, email_subject, email_body)
    
    return redirect('/task-detail/' + pk)


def add_comment(request, pk):
    comment = request.POST['comment']
    name = request.user.first_name + ' ' + request.user.last_name
    is_blank = True
    for x in comment:
        if(x != ' '):
            is_blank = False
    
    if(is_blank == False):
        comment_obj = Comment(task_id=pk, commentor_name=name, comment=comment)
        comment_obj.save()
        task = Task.objects.get(task_id=pk)
        email_subject = "New Comment: " + task.title
        if(name == task.assignor_name):
            email_body = "{} just added a new comment on Task - {}.\nLink to Task Page: http://{}:{}/task-detail/{}/".format(task.assignee_email, task.title, hostname, port, pk)
            send_notification(task.assignee_email, email_subject, email_body)
        else:
            email_body = "{} just added a new comment on Task - {}.\nLink to Task Page: http://{}:{}/task-detail/{}/".format(task.assignor_name, task.title, hostname, port, pk)
            send_notification(task.assignor_name, email_subject, email_body)
    
    return redirect('/task-detail/' + pk)


# git remote add origin git@github.com:rohan-raut/Work-Compliance-System.git
# git branch -M main
# git push -u origin main