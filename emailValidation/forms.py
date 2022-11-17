from django import forms
from.models import EmailValidations


class ProjectForm(forms.ModelForm):
    model = EmailValidations

    class Meta:
        fields = ['taskName', 'rcpt_email', 'input_file']
