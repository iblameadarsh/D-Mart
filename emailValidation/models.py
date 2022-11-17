from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class EmailValidations(models.Model):
    taskName = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    rcpt_email = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Email Field, max 255 characters.'
    )
    input_file = models.FileField(
        default='default.csv',
        upload_to='files',
        help_text='xlsx and csv files only.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.user} | {self.taskName}'
