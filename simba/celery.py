from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simba.settings')
app = Celery('simba')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'my_periodic_task': {
        'task' : 'product.routine_tasks.repeat_the_task',
        'schedule' : timedelta(seconds=5)
    },
}