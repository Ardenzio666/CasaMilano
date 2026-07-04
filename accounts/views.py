from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from accounts.task import send_activation_email_async
from legal.models import UserConsent
from .forms import CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm, LoginForm, UserRegistrationForm
from django.contrib.auth.views import LogoutView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def user_login(request):
    logger.info(
        "Login request",
        extra={
            "method": request.method,
            "ip": request.META.get("REMOTE_ADDR"),
            "xff": request.META.get("HTTP_X_FORWARDED_FOR"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
            "referer": request.META.get("HTTP_REFERER"),
            "origin": request.META.get("HTTP_ORIGIN"),
            "host": request.get_host(),
            "is_secure": request.is_secure(),
            "has_csrf_cookie": "csrftoken" in request.COOKIES,
            "has_session_cookie": "sessionid" in request.COOKIES,
        },
    )
    if request.method == 'POST':
        logger.info("Auth request received")
        form = LoginForm(request.POST)
        if form.is_valid():
            cf = form.cleaned_data
            user_record = None
            try:
                user_record = User.objects.get(email__iexact=cf['email'].strip())
                logger.info(f"User with email {user_record} is trying to authenticate")
            except User.DoesNotExist:
                logger.error(f"User {user_record} do not exists")
                pass
            if user_record:
                user = authenticate(
                    request,
                    username=user_record,
                    password=cf['password']
                )
                if user is not None:
                    try:
                        login(request, user)
                        logger.info("User is successfully authenticated")
                        return redirect('homepage:home')
                    except Exception as e:
                        logger.error(f"Problem in logging for user {user_record}")
                        logger.error(f"Trace: {e}")
                else:
                    logger.warning(
                "Login failed",
                extra={
                    "username": user_record,
                    "user_agent": request.META.get("HTTP_USER_AGENT"),
                    "has_session_cookie": "sessionid" in request.COOKIES,
                },
            )
            messages.error(request, 'Incorrect email / password')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    logger.info("Rendering the REGISTER template")
    return render(
        request,
        'accounts/register.html'
    )


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logger.info(f"Logout user: {request.user.email}")
        return super().dispatch(request, *args, **kwargs)


def register_form(request):
    logger.info("Register request received")

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            logger.info("Register form is valid")

            new_user = user_form.save(commit=False)
            new_user.is_active = False
            new_user.save()

            logger.info("Inactive user created")

            UserConsent.objects.create(
                user=new_user,
                consent_type=UserConsent.PRIVACY_POLICY,
                accepted=True,
                policy_version="1.0",
            )

            UserConsent.objects.create(
                user=new_user,
                consent_type=UserConsent.NEWSLETTER_EVENTS,
                accepted=user_form.cleaned_data["newsletter_events"],
                policy_version="1.0",
            )

            logger.info("User consents saved")

            uid = urlsafe_base64_encode(force_bytes(new_user.pk))
            token = default_token_generator.make_token(new_user)

            activation_path = reverse(
                "accounts:activate_account",
                kwargs={
                    "uidb64": uid,
                    "token": token,
                }
            )

            activation_url = request.build_absolute_uri(activation_path)

            logger.info(f"Activation url generated for user {new_user.email}")

            form_data = {
                "subject_template_name": "mails/activation_subject.txt",
                "html_template": "mails/activation_email.html",
                "to_email": new_user.email,
                "context": {
                    "first_name": new_user.first_name,
                    "activation_url": activation_url,
                },
            }

            send_activation_email_async.delay(form_data)

            logger.info(f"Activation email sent to {new_user.email}")

            return render(
                request,
                "accounts/register_done.html",
                {"new_user": new_user}
            )

    else:
        user_form = UserRegistrationForm()

    return render(
        request,
        "accounts/register_form.html",
        {"user_form": user_form}
    )

#PASSWORD CHANGE
class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("accounts:password_change_done")

    def form_valid(self, form):
        user = self.request.user
        logger.info(f"Password change SUCCESS for user: {user.email}")
        return super().form_valid(form)

    def form_invalid(self, form):
        user = self.request.user
        logger.warning(f"Password change FAILED for user: {user.email}")
        return super().form_invalid(form)
    

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logger.info(f"User {request.user.email} reached password_change_done page")
        return super().dispatch(request, *args, **kwargs)
    

#PASSWORD RESET
class CustomPasswordResetView(PasswordResetView):
    logger.info("Entering the CustomPasswordResetView")
    form_class = CustomPasswordResetForm
    template_name = "registration/password_reset_form.html"
    email_template_name = "mails/password_reset_email.txt"
    html_email_template_name = "mails/mail_template_reset_password.html"
    subject_template_name = "mails/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")
    #success_url = reverse_lazy("homepage:home")

    def form_valid(self, form):
        logger.info("CustomPasswordResetView form_valid called")
        return super().form_valid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    logger.info("Entering the CustomPasswordResetDoneView")

    template_name = "registration/password_reset_done.html"

    def get(self, request, *args, **kwargs):
        logger.info("CustomPasswordResetDoneView GET called")
        return super().get(request, *args, **kwargs)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    logger.info("Entering the CustomPasswordResetConfirmView")

    form_class = CustomSetPasswordForm
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")

    def form_valid(self, form):
        logger.info("CustomPasswordResetConfirmView form_valid called")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning("CustomPasswordResetConfirmView form_invalid called")
        logger.warning(f"Form errors: {form.errors}")
        return super().form_invalid(form)
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    logger.info("Entering the CustomPasswordResetCompleteView")

    template_name = "registration/password_reset_complete.html"

    def get(self, request, *args, **kwargs):
        logger.info("CustomPasswordResetCompleteView GET called")
        return super().get(request, *args, **kwargs)
    
@login_required
def user_management(request):
    logger.info("User management page requested")

    latest_newsletter_consent = (
        request.user.consents
        .filter(consent_type=UserConsent.NEWSLETTER_EVENTS)
        .order_by("-accepted_at")
        .first()
    )

    newsletter_enabled = (
        latest_newsletter_consent is not None
        and latest_newsletter_consent.accepted
    )

    return render(
        request,
        "accounts/user_management.html",
        {
            "newsletter_enabled": newsletter_enabled,
            "latest_newsletter_consent": latest_newsletter_consent,
        }
    )


@login_required
def delete_account(request):
    if request.method != "POST":
        logger.warning("Delete account called with non-POST method")
        return redirect("accounts:user_management")

    user = request.user
    username = user.get_username()

    logger.info("Deleting account for user=%s", username)

    logout(request)
    user.delete()

    messages.success(
        request,
        "Il tuo account è stato cancellato correttamente."
    )

    return redirect("accounts:login")


def activate_account(request, uidb64, token):
    logger.info("Account activation request received")

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        logger.error("Invalid activation link")
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        logger.info("User account activated")

        messages.success(
            request,
            "Account attivato correttamente. Ora puoi effettuare il login."
        )

        return redirect("accounts:login")

    logger.error("Invalid or expired activation token")

    return render(
        request,
        "accounts/activation_invalid.html"
    )


@login_required
def update_consents(request):
    if request.method != "POST":
        logger.warning("Update consents called with non-POST method")
        return redirect("accounts:user_management")

    newsletter_enabled = request.POST.get("newsletter_events") == "on"

    UserConsent.objects.create(
        user=request.user,
        consent_type=UserConsent.NEWSLETTER_EVENTS,
        accepted=newsletter_enabled,
        policy_version="1.0",
    )

    logger.info(
        "Newsletter consent updated for user=%s value=%s",
        request.user.email,
        newsletter_enabled,
    )

    messages.success(
        request,
        "Le preferenze privacy sono state aggiornate correttamente."
    )

    return redirect("accounts:user_management")

