from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from casamilano import settings
#import logging

#logger = logging.getLogger(__name__)

def send_email(html_template, context):
    from_email = settings.EMAIL_HOST_USER
    subject = context.get('subject')
    to_email = context.get('to_email')
    cc = context.get('cc', [])
    bcc = context.get('bcc', [])
    attachments = context.get('attachments', [])
    reply_to = context.get("reply_to", [])
    

    if not to_email:
        raise ValueError("The 'to_email' address must be provided and cannot be empty.")
    elif not isinstance(to_email, list):
        to_email = [to_email]

    if not isinstance(to_email, list):
        to_email = [to_email]

    if cc and not isinstance(cc, list):
        cc = [cc]

    if bcc and not isinstance(bcc, list):
        bcc = [bcc]

    if reply_to and not isinstance(reply_to, list):
        reply_to = [reply_to]

    try:
        html_message = render_to_string(html_template, context)
        message = EmailMessage(subject=subject, body=html_message, from_email=from_email, to=to_email, cc=cc, bcc=bcc,
                               attachments=attachments, reply_to=reply_to)
        message.content_subtype = 'html'
        for attachment in attachments:
            message.attach(*attachment)
        result = message.send()
        print(f"RESULT: {result}")
        #logger.info(f"Sending email to {', '.join(to_email)} with subject: {subject} - Status {result}")
    except Exception as e:
        print("Problemi invio mail")
        print(e)
        #logger.info(f"Sending email to {', '.join(to_email)} with subject: {subject} - Status 0")
        #logger.exception(e)