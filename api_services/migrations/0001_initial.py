# Generated by Django 4.1 on 2023-05-24 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField()),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('commentor_name', models.CharField(max_length=500)),
                ('comment', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField()),
                ('file', models.FileField(upload_to='')),
                ('uploaded_by_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Organization_Hierarchy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_role', models.CharField(max_length=200)),
                ('priority', models.IntegerField()),
                ('show_report', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.IntegerField(primary_key=True, serialize=False)),
                ('assignor_name', models.CharField(max_length=500)),
                ('assignor_email', models.EmailField(max_length=254)),
                ('assignee_name', models.CharField(max_length=500)),
                ('assignee_email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=1000)),
                ('deadline', models.DateTimeField()),
                ('status', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('user_role', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
