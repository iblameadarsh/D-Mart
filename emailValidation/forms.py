from django import forms
from .models import ValidEmailExport


class EmailExportModelform(forms.ModelForm):
    class Meta:
        model = ValidEmailExport
        fields = [
            'task_name',
            'supplier_emails_file',
        ]

    def __init__(self, *args, **kwargs):
        super(EmailExportModelform, self).__init__(*args, **kwargs)
