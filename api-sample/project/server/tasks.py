import os
import time
import requests, json

from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 5)
    return True

@celery.task(name="receive_async_task")
#def receive_async_task(url, type):
def receive_async_task(url):
    
    print("receive_async_task url : "+url)
    #print("receive_async_task type : "+type)
    
    #time.sleep(int(type)*5)
    time.sleep(1*5)
    return url

@celery.task(name="callback_task")
def callback_task(url):
    
    # url = final_result_callback+"/?"+flow_job_id
    # url = callback_uri = service_async_receiver_uri+"/?"+flow_job_id
    print("callback_task url : "+url)
    # return requests.get(url).text
    target_url = url.split('?')[0]
    flow_job_id = url.split('?')[1]
    temp_host = 'svc-async-receiver.flowmanager.example.com'
    
    print("callback_task target_url : "+target_url)
    print("callback_task flow_job_id : "+flow_job_id)
    
    headers = {'Content-Type': 'application/json; charset=utf-8', 'Host': temp_host}
    
    payload = { 
        "flow_job_id": flow_job_id,
        "result": "reult__"+url
    }
    payload_json = json.dumps(payload)
    return requests.post(target_url, headers=headers, data=payload_json).text

