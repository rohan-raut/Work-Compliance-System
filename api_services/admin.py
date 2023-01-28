from django.contrib import admin
from api_services.models import Account, Tasks, Files, Comments

# Register your models here.

admin.site.register(Account)
admin.site.register(Tasks)
admin.site.register(Files)
admin.site.register(Comments)
