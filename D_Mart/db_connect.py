from pymongo import MongoClient
from django.conf import settings


class DATABASE:

    def __init__(self):
        self.client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

        # Mongo Database for GUI Executions Data Exports
        db_gui = self.client.d_mart_emails

        # Collection for Email Validation Exports
        EXPORT_EMAIL_VALIDATIONS_INDEX = [("task_id", 1), ]
        self.email_validation_exports = db_gui.email_validation_exports
        self.email_validation_exports.create_index(EXPORT_EMAIL_VALIDATIONS_INDEX)