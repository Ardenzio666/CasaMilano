from django.shortcuts import redirect, render

from casamilano import settings
from contatti.forms import ContactForm
from contatti.mail_utils import send_email



def contatti(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print("Form received")
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            email_handler(form.cleaned_data, request)
            #messages.success(request, "Messaggio inviato correttamente.")
            return redirect("contatti:contatti")
        else:
            print("Form is not valid")

    else:
        form = ContactForm()
    return render(
        request,
        'contatti.html'
    )

def email_handler(form_data, request):
    print("Email handler")
    template = 'mails/mail_template.html'
    print(settings.CONTACT_RECEIVER_EMAIL)
    context = {
        'subject': f"[Contatti] {form_data['subject']}",
        'to_email': settings.CONTACT_RECEIVER_EMAIL,  # TU
        'reply_to': form_data['email'],  # UTENTE
        'name': form_data['name'],
        'email': form_data['email'],
        'message': form_data['message'],
        'base_uri': request.build_absolute_uri("/").rstrip("/"),
    }

    send_email(template, context)



