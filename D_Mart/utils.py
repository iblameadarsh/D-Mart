import os
import random
import string
import uuid

from django.conf import settings


def get_a_to_z_upload_path(sub_folder, filename):
    ext = filename.split(".").pop()
    folder = random.choice(string.ascii_lowercase)
    name = '%s_%s' % (folder, uuid.uuid4().hex)
    folder_path = os.path.join(settings.MEDIA_SUB_FOLDER_NAME, sub_folder, folder)
    folder_root = os.path.join(settings.MEDIA_ROOT, folder_path)
    if not os.path.exists(folder_root):
        os.makedirs(folder_root)
    return os.path.join(folder_path, '%s.%s' % (name, ext))


def import_file_path(instance, filename):
    return get_a_to_z_upload_path('import_file_path', filename)


# MODEL_UTILS

TASK_STATUS_CHOICES = (
    ("pending", 'pending'),
    ("running", 'running'),
    ("terminated", 'terminated'),
    ("completed", 'completed'),
)
