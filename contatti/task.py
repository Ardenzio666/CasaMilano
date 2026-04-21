from celery import shared_task
import logging
from contatti.mail_utils import email_handler

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def send_mail_async(self, form_data):
    mail_logger = logging.getLogger("mail_logger")
    mail_logger.info("CELERY TASK TO EXECUTE: email_handler")
    try:
        email_handler(form_data)
    except Exception as e:
        mail_logger.exception("Email handler failed execution")
    mail_logger.info("CELERY EXECUTED: email_handler")