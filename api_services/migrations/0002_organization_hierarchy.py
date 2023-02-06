# Generated by Django 4.1 on 2023-02-01 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization_Hierarchy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_role', models.CharField(max_length=200)),
                ('priority', models.IntegerField()),
                ('show_report', models.BooleanField(default=False)),
            ],
        ),
    ]
