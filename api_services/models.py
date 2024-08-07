from enum import unique
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from traitlets import default

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, user_role, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not user_role:
            raise ValueError("User must have a role defined")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            user_role = user_role
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    
    def create_superuser(self, email, username, first_name, last_name, user_role, password):
        user = self.create_user(
            email = email,
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            user_role = user_role
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)
        return user



class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=254, unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_role = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "user_role"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perm(self, app_label):
        return True



# Task database model
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    assignor_name = models.CharField(max_length=500)
    assignor_email = models.EmailField()
    assignee_name = models.CharField(max_length=500)
    assignee_email = models.EmailField()    
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    draft_date = models.DateField(auto_now=True)   # when task is created
    deadline = models.DateField()
    publish_date = models.DateField(null=True) # when task is submitted
    status = models.CharField(max_length=100)

'''
Task join with account on user_role -> result & assignee_email


'''




# class NewDeadline(models.Model):
#     task_id = models.IntegerField()
#     old_deadline = models.DateTimeField()
#     new_deadline = models.DateTimeField()
#     reason = models.CharField()



# File database for every tasks
class File(models.Model):
    task_id = models.IntegerField()
    file = models.FileField()
    uploaded_by_email = models.EmailField()             # email of assignee or assignor


# Comments for each tasks
class Comment(models.Model):
    task_id = models.IntegerField()
    date_time = models.DateTimeField(auto_now=True)
    commentor_name = models.CharField(max_length=500)
    comment = models.CharField(max_length=2000)



# Token generation while user is registered
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



# Hierarchy model
class Organization_Hierarchy(models.Model):
    user_role = models.CharField(max_length=200)
    priority = models.IntegerField()
    show_report = models.BooleanField(default=False)