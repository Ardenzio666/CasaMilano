from django.shortcuts import redirect, render
from django.contrib import messages
from casamilano import settings
from contatti.forms import ContactForm
from contatti.mail_utils import send_email
from contatti.task import send_mail_async
import logging
logger = logging.getLogger(__name__)

def contatti(request):
    logger.info("Entering CONTATTI views")
    if request.method == "POST":
        logger.info("request method is POST")
        form = ContactForm(request.POST)
        if form.is_valid():
            logger.info("Form is valid")
            try:
                logger.info("sending mails with celery")
                send_mail_async.delay(form.cleaned_data)
                messages.success(request, "Abbiamo ricevuto il tuo messaggio. Ti risponderemo presto. Se non vedi la nostra mail, per favore controlla nello spam. Grazie per averci contattato!!")
            except Exception as e:
                messages.error(
                    request,
                    "Si è verificato un errore durante l'invio. Riprova più tardi."
                )
                logger.exception("Si è verificato un errore durante l'invio.")
            return redirect("contatti:contatti")
        else:
            messages.warning(
                request,
                "Controlla i campi del form e riprova."
            )
            logger.warning("Form is not valid")

    else:
        logger.info("Request method is GET")
        form = ContactForm()
    return render(
        request,
        'contatti.html'
    )





