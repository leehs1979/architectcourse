import os
import time
import requests

from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 5)
    return True

@celery.task(name="receive_async_task")
def receive_async_task(url):
    time.sleep(10)
    return url

@celery.task(name="callback_task")
def callback_task(url):
    print("callback_task : "+url)
    return requests.get('http://www.naver.com').text

