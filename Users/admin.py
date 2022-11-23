from django.contrib import admin
from .models import ActivityLogs


# Register your models here.


class LogAdminView(admin.ModelAdmin):
    search_fields = ("description",)
    list_display = ("log_type", "description", "user", "created_at")
    list_filter = ('log_type', "user", 'created_at')


admin.site.register(ActivityLogs, LogAdminView)
