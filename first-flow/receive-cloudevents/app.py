from flask import Flask, request, jsonify

from cloudevents.http import from_http
import requests,json

app = Flask(__name__)


# create an endpoint at http://localhost:/3000/
@app.route("/", methods=["POST"])
def home():
    # create a CloudEvent
    event = from_http(request.headers, request.get_data())

    # you can access cloudevent fields as seen below
    #print(
    #    f"Found {event['id']} from {event['source']} with type "
    #    f"{event['type']} and specversion {event['specversion']}"
    #)
    #message = event.data['message']
    targetURL = event.data['targetURL']
    targetAPI = event.data['targetAPI']
    headers = event.data['headers']
    body = event.data['body']

    print(targetURL)
    print(targetAPI)
    json_body=json.dumps(body)
    print(headers)
    print(json_body)

    #response = requests.get(targetURL+targetAPI)
    response = requests.post(targetURL+targetAPI, data=json_body, headers=headers)
    print(response.text,flush=True)

    return "", 204

@app.route("/hello")
def hello():
    return 'hello'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8001)
