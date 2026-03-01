# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vru*47tq9@d9auv(aqxf6r-l-_h!817#y3fw7i29o+h=9w&7)h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'casamilano',
        'USER': 'casamilanoadmin',
        'PASSWORD': 'Porcino1!',
        'HOST': 'localhost'
    }
}