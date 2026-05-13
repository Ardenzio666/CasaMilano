from django.shortcuts import redirect, render
from django.contrib import messages
from casamilano import settings
from contatti.forms import ContactForm
from contatti.task import send_mail_async
import logging

from contatti.turnstile_helper import verify_turnstile_token
logger = logging.getLogger(__name__)

def contatti(request):
    logger.info("Entering CONTATTI views")
    context = {
        "turnstile_site_key": settings.CLOUDFLARE_TURNSTILE_SITE_KEY,
    }

    if request.method == "POST":
        turnstile_token = request.POST.get("cf-turnstile-response")
        ip = request.META.get("REMOTE_ADDR")
        form = ContactForm(request.POST)

        if not verify_turnstile_token(turnstile_token, ip):
            form.add_error(None, "Verifica anti-spam non riuscita. Riprova.")
            return render(request, "contatti/contatti.html", {
                "form": form,
                "turnstile_site_key": settings.CLOUDFLARE_TURNSTILE_SITE_KEY,
            })
        logger.info("request method is POST")
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
        'contatti.html',
        context
    )





