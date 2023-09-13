import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simba.settings")

app = Celery("simba")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

