# project/server/main/views.py
import os
import time
from project.server.tasks import create_task, receive_async_task, callback_task
from celery.result import AsyncResult


from flask import render_template, Blueprint, jsonify, request

main_blueprint = Blueprint("main", __name__,)


@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("main/home.html")


@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    content = request.json
    task_type = content["type"]
    # Add Celery
    task = create_task.delay(int(task_type))
    return jsonify({"task_id": task.id, "result": task.id}), 202


# Result API Call 방식 : Client에서 Polling 방식으로 상태 체크
@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
        "result": task_result.result
    }
    return jsonify(result), 200

@main_blueprint.route("/callback_tasks", methods=["POST"])
def run_callback():
    content = request.json
    print(content)

    callback_uri = content["callback_uri"]

    # Add Celery
    task = receive_async_task.apply_async([callback_uri], link=[callback_task.s()]) 
    return jsonify({"task_id": task.id, "result": task.id}), 202


## add by infordb
@main_blueprint.route("/sync_tasks/<api_id>", methods=["GET"])
def run_sync_api(api_id):
    time.sleep(1)
    result = {
        #"api_id": api_id
        "result": api_id
    }
    return jsonify(result), 200


@main_blueprint.route("/callback_tasks/<api_id>", methods=["POST"])
def run_callback_api(api_id):
    content = request.json
    print("callback_tasks : ")
    print(content)

    callback_uri = content["callback"]
    api_input = content["api_input"]

    # Add Celery
    task = receive_async_task.apply_async([callback_uri, api_input], link=[callback_task.s()]) 

    result = {
        "task_id": task.id,
        "result": api_id
    }

    return jsonify(result), 202
