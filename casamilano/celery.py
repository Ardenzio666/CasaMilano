import logging
import os
from celery import Celery
from celery.signals import setup_logging

@setup_logging.connect
def config_loggers(*args, **kwargs):
    from django.conf import settings
    logging.config.dictConfig(settings.LOGGING)
    
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "casamilano.settings")

app = Celery("casamilano_project")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()