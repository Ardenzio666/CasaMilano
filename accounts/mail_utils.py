import logging
from django.conf import settings
from django.template import loader
from django.conf import settings
from contatti.mail_utils import send_email_sendgrid


def email_handler_reset_password(form_data: dict):
    mail_logger = logging.getLogger("mail_logger")
    mail_logger.info("Entering function email_handler_reset_password")

    subject_template_name = form_data.get("subject_template_name")
    html_template = form_data.get("html_template")
    context = form_data.get("context", {})
    to_email = form_data.get("to_email")

    if not subject_template_name:
        raise ValueError("Missing subject_template_name for password reset email")

    if not html_template:
        raise ValueError("Missing html_template for password reset email")

    if not to_email:
        raise ValueError("Missing to_email for password reset email")

    subject = loader.render_to_string(
        subject_template_name,
        context,
    )
    subject = "".join(subject.splitlines())

    context.update({
        "subject": subject,
        "to_email": to_email,
        "logo_path": str(settings.BASE_DIR / "static" / "homepage" / "img" / "logo.png"),
    })

    mail_logger.info(f"Password reset email prepared for: {to_email}")
    mail_logger.info(f"Password reset template: {html_template}")

    status_code = send_email_sendgrid(
        html_template=html_template,
        context=context,
    )

    mail_logger.info(f"Password reset email sent with status code: {status_code}")

    return status_code


def email_handler_activation(form_data: dict):
    mail_logger = logging.getLogger("mail_logger")
    mail_logger.info("Entering function email_handler_activation")

    subject_template_name = form_data.get("subject_template_name")
    html_template = form_data.get("html_template")
    context = form_data.get("context", {})
    to_email = form_data.get("to_email")

    if not subject_template_name:
        raise ValueError("Missing subject_template_name for activation email")

    if not html_template:
        raise ValueError("Missing html_template for activation email")

    if not to_email:
        raise ValueError("Missing to_email for activation email")

    subject = loader.render_to_string(
        subject_template_name,
        context,
    )
    subject = "".join(subject.splitlines())

    context.update({
        "subject": subject,
        "to_email": to_email,
        "logo_path": str(settings.BASE_DIR / "static" / "homepage" / "img" / "logo.png"),
    })

    mail_logger.info(f"Activation email prepared for: {to_email}")
    mail_logger.info(f"Activation template: {html_template}")

    status_code = send_email_sendgrid(
        html_template=html_template,
        context=context,
    )

    mail_logger.info(f"Activation email sent with status code: {status_code}")

    return status_code