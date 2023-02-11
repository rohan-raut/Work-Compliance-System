from django.contrib import admin
from api_services.models import Account, Task, File, Comment, Organization_Hierarchy

# Register your models here.

admin.site.register(Account)
admin.site.register(Task)
admin.site.register(File)
admin.site.register(Comment)
admin.site.register(Organization_Hierarchy)
