from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(ValidEmailExport)


class EmailExportAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_name', 'user', 'created_at', 'status')
    list_filter = ("user", "status", "created_at")
