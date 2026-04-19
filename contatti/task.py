from celery import shared_task

from contatti.mail_utils import email_handler

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def send_mail_async(self, form_data):
    print("send mail async")
    email_handler(form_data)