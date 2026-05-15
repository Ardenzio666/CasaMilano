import logging

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
from django.template import loader
from django.utils.html import strip_tags

from accounts.task import send_password_reset_email_async

class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
)
    
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })

class UserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(
        label="Ripeti password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    privacy_policy = forms.BooleanField(
        required=True,
        label="Ho letto e accetto la Privacy Policy",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    newsletter_events = forms.BooleanField(
        required=False,
        label="Desidero ricevere comunicazioni sugli eventi di Casa Milano",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Esiste già un account con questa email.")

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error("password2", "Le password non coincidono.")

        return cleaned_data
    
    # ✅ hashing password
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # importante!
        user.set_password(self.cleaned_data['password'])  # 🔥 hashing
        if commit:
            user.save()
        return user
    
class CustomPasswordResetForm(PasswordResetForm):

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        mail_logger = logging.getLogger("mail_logger")
        mail_logger.info("CustomPasswordResetForm.send_mail called for %s", to_email)
        safe_context = {
            "email": context.get("email"),
            "domain": context.get("domain"),
            "site_name": context.get("site_name"),
            "uid": context.get("uid"),
            "token": context.get("token"),
            "protocol": context.get("protocol"),
            "username": context.get("user").get_username() if context.get("user") else "",
        }

        form_data = {
            "subject_template_name": subject_template_name,
            "html_template": html_email_template_name or email_template_name,
            "context": safe_context,
            "to_email": to_email,
        }
        mail_logger.info("Password reset task queued for %s", to_email)
        send_password_reset_email_async.delay(form_data)

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nuova password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Inserisci nuova password"
        })
    )

    new_password2 = forms.CharField(
        label="Conferma password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Ripeti nuova password"
        })
    )