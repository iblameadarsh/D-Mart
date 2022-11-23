from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.

LOG_TYPES = (
    ("file_export", "FILE_EXPORT"),
    ("login", "LOGIN"),
    ("logout", "LOGOUT"),
    ("task_created", "TASK_CREATED"),
    ("task_terminate", "TASK_TERMINATE"),
    ("page_view", "PAGE_VIEW")
)


class CreatedAtUpdatedAtMixin(models.Model):
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True,
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        _('Updated At'),
        auto_now=True,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class ActivityLogs(CreatedAtUpdatedAtMixin, models.Model):
    log_type = models.CharField(
        _('Log Type'),
        help_text=_('Your log type'),
        max_length=254, choices=LOG_TYPES)

    description = models.TextField(
        _('Description'),
        help_text=_('log Description in detail'),
        blank=True, default='')

    user = models.ForeignKey(
        User,
        related_name='log_for_user',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('User Activity Log')
        verbose_name_plural = _('User Activity Logs')

    def __str__(self):
        return self.log_type
