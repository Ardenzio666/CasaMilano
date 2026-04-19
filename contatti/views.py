from django.shortcuts import redirect, render
from django.contrib import messages
from casamilano import settings
from contatti.forms import ContactForm
from contatti.mail_utils import send_email
from contatti.task import send_mail_async



def contatti(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print("Form received")
            try:
                send_mail_async.delay(form.cleaned_data)
                messages.success(request, "Abbiamo ricevuto il tuo messaggio. Ti risponderemo presto. Se non vedi la nostra mail, per favore controlla nello spam. Grazie per averci contattato!!")
            except Exception as e:
                messages.error(
                    request,
                    "Si è verificato un errore durante l'invio. Riprova più tardi."
                )
                print(e)
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





