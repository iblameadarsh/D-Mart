from celery import shared_task


@shared_task(bind=True)
def run_export():
    print('testrun')
    pass
