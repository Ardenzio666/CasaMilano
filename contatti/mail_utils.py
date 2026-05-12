import base64
from email.mime.image import MIMEImage
from pathlib import Path

from django.template.loader import render_to_string
from django.core.mail import  EmailMultiAlternatives
from django.utils.html import strip_tags
from casamilano import settings
import logging
import base64
import mimetypes
from pathlib import Path

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
    ContentId,
    ReplyTo,
)

mail_logger = logging.getLogger("mail_logger")
def _ensure_list(value):
    if not value:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _build_file_attachment(file_path: str, disposition: str = "attachment", content_id: str | None = None) -> Attachment | None:
    mail_logger.info("_build_file_attachment function")
    mail_logger.info(f"file path: {file_path}")
    path = Path(file_path)

    try:
        with path.open("rb") as f:
            encoded_file = base64.b64encode(f.read()).decode()

        mime_type, _ = mimetypes.guess_type(path.name)
        mime_type = mime_type or "application/octet-stream"

        attachment = Attachment(
            FileContent(encoded_file),
            FileName(path.name),
            FileType(mime_type),
            Disposition(disposition),
        )

        if content_id:
            attachment.content_id = ContentId(content_id)
    except Exception as e:
        mail_logger.exception("Prolem in building file attachment")
        return None
    mail_logger.info("file attachment successfully built")
    return attachment


def _build_tuple_attachment(attachment_data) -> Attachment | None:
    """
    Supporta attachment nel formato:
    (filename, content, mime_type)

    dove content può essere:
    - str
    - bytes
    """
    mail_logger.info("Entering the _build_tuple_attachment function")
    try:
        if len(attachment_data) != 3:
            raise ValueError(
                "Gli attachment come tuple/list devono avere formato: (filename, content, mime_type)"
            )

        filename, content, mime_type = attachment_data

        if isinstance(content, str):
            content = content.encode("utf-8")

        encoded_file = base64.b64encode(content).decode()
        mime_type = mime_type or "application/octet-stream"

        attachment = Attachment(
            FileContent(encoded_file),
            FileName(filename),
            FileType(mime_type),
            Disposition("attachment"),
        )
    except Exception as e:
        mail_logger.exception("Problem builnding attachment")
        return None
    
    return attachment

def send_email_sendgrid(html_template, context):
    mail_logger.info("Entering function send_email_sendgrid")

    from_email = settings.DEFAULT_FROM_EMAIL
    subject = context.get("subject")
    to_email = context.get("to_email")
    cc = context.get("cc", [])
    bcc = context.get("bcc", [])
    attachments = context.get("attachments", [])
    reply_to = context.get("reply_to", [])
    logo_path = context.get("logo_path", "")

    mail_logger.info(f"from_email: {from_email}")
    mail_logger.info(f"subject: {subject}")
    mail_logger.info(f"to_email: {to_email}")
    mail_logger.info(f"cc: {cc}")
    mail_logger.info(f"bcc: {bcc}")
    mail_logger.info(f"attachments: {attachments}")
    mail_logger.info(f"reply_to: {reply_to}")
    mail_logger.info(f"logo_path: {logo_path}")

    if not to_email:
        raise ValueError("The 'to_email' address must be provided and cannot be empty.")

    to_email = _ensure_list(to_email)
    cc = _ensure_list(cc)
    bcc = _ensure_list(bcc)
    reply_to = _ensure_list(reply_to)

    try:
        html_message = render_to_string(html_template, context)
        text_message = strip_tags(html_message)

        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=text_message,
            html_content=html_message,
        )

        if cc:
            message.cc = cc

        if bcc:
            message.bcc = bcc

        if reply_to:
            message.reply_to = ReplyTo(reply_to[0])

        for attachment in attachments:
            if isinstance(attachment, (list, tuple)):
                message.add_attachment(_build_tuple_attachment(attachment))
            else:
                message.add_attachment(_build_file_attachment(attachment))

        if logo_path:
            message.add_attachment(
                _build_file_attachment(
                    logo_path,
                    disposition="inline",
                    content_id="logo",
                )
            )
        mail_logger.info("Sending mail with SENDGRID api client")
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)

        mail_logger.info(f"RESULT: {response.status_code}")
        mail_logger.info(response.body)
        mail_logger.info(response.headers)

        return response.status_code

    except Exception as e:
        mail_logger.exception("Problemi invio mail")
        raise e


def email_handler(form_data):
    mail_logger.info("Entering function: Email handler")
    template = 'mails/mail_template.html'
    context = {
        'subject': f"[Contatti] {form_data['subject']}",
        'to_email': settings.CONTACT_RECEIVER_EMAIL,  # TU
        'reply_to': form_data['email'],  # UTENTE
        'name': form_data['name'],
        'email': form_data['email'],
        'message': form_data['message'],
    }
    mail_logger.info("Sending mail to casa milano")
    send_email_sendgrid(template, context)
    mail_logger.info("Sending mail to client")
    send_email_sendgrid(
        html_template='mails/reply_mail_template.html',
        context={
            'subject': "Grazie per averci contattato",
            'to_email': form_data['email'],
            'name': form_data['name'],
            'message': form_data['message'],
            'logo_path': Path(settings.BASE_DIR) / "static" / "homepage" / "img" / "logo.png"
        }
    )

def load_img_data_uri(graph_path: Path | str) -> str | None:
    """Load image and return an inline PNG Data URI."""
    if isinstance(graph_path, str):
        graph_path = Path(graph_path)
    if not graph_path.exists():
        return None

    try:
        logo_bytes = graph_path.read_bytes()
    except OSError:
        return None

    if not logo_bytes:
        return None

    encoded_logo = base64.b64encode(logo_bytes).decode("ascii")
    return f"data:image/png;base64,{encoded_logo}"