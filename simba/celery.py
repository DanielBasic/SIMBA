from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, shared_task
from celery.schedules import crontab, schedule, timedelta
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simba.settings')
app = Celery('simba')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "my-periodic-task": {
        "task": "show",
        "schedule": schedule(run_every=timedelta(seconds=5)), 
    },
}


@shared_task(name='show')
def show():
    from datetime import timedelta
    now = datetime.datetime.now().isoformat()
    print(now)


