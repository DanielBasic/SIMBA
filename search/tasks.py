from celery import shared_task
from time import sleep

@shared_task
def task_one():
    sleep(20)

