import os
from dotenv import load_dotenv

def str_to_bool(value: str) -> bool:
    if value is None:
        return False
    
    return value.strip().lower() in ("true", "1", "yes", "y", "on")

load_dotenv()
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY","")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str_to_bool(os.environ.get("DEBUG","False"))

ALLOWED_HOSTS = ["127.0.0.1", "localhost","167.71.52.149", "casamilano69.it","www.casamilano69.it"]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': 'localhost'
    }
}

#Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.libero.it'  # Replace with your SMTP host
EMAIL_HOST_USER = "casamilano69@libero.it"  # Your email address
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")  # Your email password
EMAIL_PORT = 465  # SMTP port
EMAIL_USE_SSL = True  # Use SSL for secure connection
#CONTACT_RECEIVER_EMAIL = 'casamilano69@libero.it'
import os

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
CONTACT_RECEIVER_EMAIL = os.getenv("CONTACT_RECEIVER_EMAIL")

#CLOUDFLARE
CLOUDFLARE_TURNSTILE_SITE_KEY = os.getenv("CLOUDFLARE_TURNSTILE_SITE_KEY")
CLOUDFLARE_TURNSTILE_SECRET_KEY = os.getenv("CLOUDFLARE_TURNSTILE_SECRET_KEY")

#SECURITY
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"