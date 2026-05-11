from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm, LoginForm, UserRegistrationForm
from django.contrib.auth.views import LogoutView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
import logging

logger = logging.getLogger(__name__)

def user_login(request):
    if request.method == 'POST':
        logger.info("Auth request received")
        form = LoginForm(request.POST)
        if form.is_valid():
            cf = form.cleaned_data
            user_record = None
            try:
                user_record = User.objects.get(email=cf['email'])
                logger.info(f"User with email {user_record} is trying to authenticate")
            except User.DoesNotExist:
                pass
            if user_record:
                user = authenticate(
                    request,
                    username=user_record,
                    password=cf['password']
                )
                if user is not None:
                    login(request, user)
                    logger.info("User is successfully authenticated")
                    return redirect('homepage:home')
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
    logger.info("Register request receiced")
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            logger.info("Register form is valid")
            cf = user_form.cleaned_data
            email = cf['email']
            password = cf['password']
            password2 = cf['password2']
            if password == password2:
                logger.info("Passwords matcht")
                if User.objects.filter(email=email).exists():
                    logger.error("User email already exists")
                    messages.error(request,
                        'User with given email already exists')
                    return render(
                        request,
                        'accounts/register_form.html',
                        {'user_form': user_form}
                    )
            else:
                logger.error("Passwords mismatch")
                messages.error(request, 'Passwords don\'t match')
                return render(
                    request,
                    'accounts/register_form.html',
                    {'user_form': user_form}
                )
            # Create a new user object
            new_user = User.objects.create_user(
                first_name=cf['first_name'],
                last_name=cf['last_name'],
                username=email,
                email=email,
                password=password
            )
            logger.info("User created")
            return render(
                request,
                'accounts/register_done.html',
                {'new_user': new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'accounts/register_form.html',
        {'user_form': user_form}
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

