import json

from celery import shared_task
import logging

from accounts.mail_utils import email_handler_activation, email_handler_reset_password

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def send_password_reset_email_async(self, form_data):
    mail_logger = logging.getLogger("mail_logger")
    mail_logger.info("CELERY TASK TO EXECUTE: send_password_reset_email_async")
    mail_logger.info(f"FORM DATA: {form_data}")
    try:
        email_handler_reset_password(form_data)
    except Exception as e:
        mail_logger.exception("email_handler_reset_password failed execution")
        raise
    mail_logger.info("CELERY EXECUTED: email_handler_reset_password")


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3}
)
def send_activation_email_async(self, form_data):
    mail_logger = logging.getLogger("mail_logger")
    mail_logger.info("CELERY TASK TO EXECUTE: send_activation_email_async")
    mail_logger.info(f"FORM DATA: {form_data}")

    try:
        email_handler_activation(form_data)
    except Exception:
        mail_logger.exception("email_handler_activation failed execution")
        raise

    mail_logger.info("CELERY EXECUTED: email_handler_activation")