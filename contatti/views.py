from django.shortcuts import redirect, render
from django.contrib import messages
from casamilano import settings
from contatti.forms import ContactForm
from contatti.mail_utils import send_email



def contatti(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print("Form received")
            try:
                email_handler(form.cleaned_data, request)
                messages.success(request, "Abbiamo ricevuto il tuo messaggio. Ti risponderemo presto. Se non vedi la nostra mail, per favore controlla nello spam. Grazie per averci contattato!!")
            except Exception:
                messages.error(
                    request,
                    "Si è verificato un errore durante l'invio. Riprova più tardi."
                )
            return redirect("contatti:contatti")
        else:
            messages.warning(
                request,
                "Controlla i campi del form e riprova."
            )
            print("Form is not valid")

    else:
        form = ContactForm()
    return render(
        request,
        'contatti.html'
    )

def email_handler(form_data, request):
    print("Email handler")
    base_uri = request.build_absolute_uri("/").rstrip("/")
    template = 'mails/mail_template.html'
    print(settings.CONTACT_RECEIVER_EMAIL)
    context = {
        'subject': f"[Contatti] {form_data['subject']}",
        'to_email': settings.CONTACT_RECEIVER_EMAIL,  # TU
        'reply_to': form_data['email'],  # UTENTE
        'name': form_data['name'],
        'email': form_data['email'],
        'message': form_data['message'],
        'base_uri': base_uri,
    }

    send_email(template, context)

    send_email(
        html_template='mails/reply_mail_template.html',
        context={
            'subject': "Grazie per averci contattato",
            'to_email': form_data['email'],
            'name': form_data['name'],
            'message': form_data['message'],
            'base_uri': base_uri,
        }
    )



