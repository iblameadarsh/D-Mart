from django.urls import path
from .views import *


app_name = 'emailValidation'

urlpatterns = [

    # Email Validation and export links.
    path('create-email-validation-task/', EmailValidationView.as_view(), name='email_input_form'),
    path('email-validation-task-list/', EmailTaskListView.as_view(), name='email_export_list_view'),
    path(r'export-valid-emails-view/<slug:task_id>', EmailFinalExport.as_view(),
         name='export_valid_emails'),
    path(r'export-template-file/', download_template, name='export_email_template'),
]
