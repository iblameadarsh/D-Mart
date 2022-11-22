from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import D_Mart.settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'D_Mart.settings')

app = Celery('D_Mart')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print('Request!: {0!r}'.format(self.request))
#

# app.conf.beat_schedule = {
#
# }
