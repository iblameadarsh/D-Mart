from celery import shared_task


@shared_task
def evalidationHandler(task_export_id, emails_file_path):
    from emailValidation.models import ValidEmailExport
    from emailValidation.supplier_email_verify import export_runner
    from django.core.mail import send_mail
    from D_Mart.settings import EMAIL_HOST_USER

    ValidEmailExport.objects.filter(pk=int(task_export_id)).update(status='running')
    export_runner(task_export_id, emails_file_path)
    ValidEmailExport.objects.filter(pk=int(task_export_id)).update(status='completed')
    model_obj = ValidEmailExport.objects.get(pk=int(task_export_id))
    recpt_mail = str(model_obj.user.email)
    send_mail(
        "D-Mart: Email Verification Export",
        '''Greetings,

        Your export file is ready! You can download it from your dashboard.
        Thanks & Regards''',
        EMAIL_HOST_USER,
        [recpt_mail],
        fail_silently=False,
    )