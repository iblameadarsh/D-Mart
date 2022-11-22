from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from D_Mart.utils import import_file_path, TASK_STATUS_CHOICES
from .tasks import evalidationHandler
from D_Mart import settings
import pandas as pd

# Create your models here.


class ValidEmailExport(models.Model):
    task_name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('Task name must be unique, cannot be blank!')
    )
    user = models.ForeignKey(
        User,
        related_name='exported_emails_by_user',
        on_delete=models.CASCADE
    )
    supplier_emails_file = models.FileField(
        default='default.csv',
        upload_to=import_file_path,
        help_text='Upload .csv files only, with column: '
                  'email or download template for reference '
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    status = models.CharField(
        _('Task Status'),
        max_length=100,
        choices=TASK_STATUS_CHOICES,
        default='pending'
    )
    executed_comments = models.TextField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Email Verification Exports')
        verbose_name_plural = _('Email Verification Export')

    def __str__(self):
        return self.task_name

    def check_input_file(self):
        emails_file_path = str(settings.MEDIA_ROOT) + '/' + str(self.supplier_emails_file)
        terminate = False
        input_file_check = True

        error_items = []
        columns_required = ['supplier_id', 'supplier name', 'email']
        # columns_required = ['email']

        if str(self.supplier_emails_file).strip() == '':
            input_file_check = False

        if input_file_check is True:
            try:
                df = pd.read_csv(emails_file_path)
            except:
                df = None
                error_items.append('Input file is invalid!')
                error_items.append(f'File used to process: {self.supplier_emails_file}')
                terminate = True
        if terminate is False:
            if df is not None:
                missing_col = []
                found_columns = list(df.columns)
                for col_val in columns_required:
                    if col_val not in found_columns:
                        missing_col.append(col_val)
                if len(missing_col) > 0:
                    terminate = True
                    error_items.append(f'Missing Columns in csv: {",".join(missing_col)}')

        if terminate is False:
            df = df.fillna('')
            email_list = df['email'].tolist()
            nun_email = 0
            for i in email_list:
                if i == '':
                    nun_email += 1
            if nun_email == len(email_list):
                terminate = True
                error_items.append('Missing values in column: email')

        if terminate is False:
            evalidationHandler.apply_async((self.id, emails_file_path),
                                           countdown=1)
        else:
            self.status = 'Terminated'
            self.executed_comments = "\n\n".join(error_items)
            self.save()
