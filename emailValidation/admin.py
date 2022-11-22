from django.contrib import admin
from .models import *

# Register your models here.


class ValidEmailExportAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_name', 'user', 'status', 'created_at')
    list_filter = ("status", "created_at", "user")


admin.site.register(ValidEmailExport, ValidEmailExportAdmin)


