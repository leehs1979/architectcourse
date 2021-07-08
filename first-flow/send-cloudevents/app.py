from flask import Flask, request, jsonify
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
import flask_restful
from flask_restx import Resource, Api
import requests,json

app = Flask(__name__)
api = Api(app)


@api.route('/test')
class TestEvent(Resource):
    def get(self):
        return {"message" : "Welcome, Get Event"}
    def post(self):
        return {"message" : "Welcome, Post Event"}

@api.route('/sync')  # url pattern으로 name 설정
class SyncTasks(Resource):
    def get(self):  
        req_data = request.get_json()
        api_uri = req_data['api_uri']
        headers = req_data['headers']
        body = req_data['body']
        print(headers)
        print(body)

        res = requests.get(api_uri, headers=headers, data=body)
        #print(res.json())
        return res.json()

    def post(self):  
        req_data = request.get_json()
        api_uri = req_data['api_uri']
        headers = req_data['headers']
        body = req_data['body']
        print(headers)
        print(body)
        json_data=json.dumps(body)

        res = requests.post(api_uri, headers=headers, data=json_data)
        
        return res.json()

@api.route('/async')  # url pattern으로 name 설정
class ASyncTasks(Resource):
    def post(self):  
        type_header = request.headers.get('Content-type')
        print(type_header)
        
        headers = {
                'Ce-Id': '536808d3-88be-4077-9d7a-a3f162705f79',
                'Ce-specversion': '0.3',
                'Ce-Type': 'dev.knative.samples.t2',
                'Ce-Source': 'dev.knative.samples/t2',
                'Content-Type': 'application/json'
        }

        data = request.get_json()
        #data = '{"targetURL": "http://35.226.56.118", "targetAPI": "/test"}'
        json_data=json.dumps(data)
        print(json_data)

        res=requests.post("http://broker-ingress.knative-eventing.svc.cluster.local/default/kafka-backed-broker", headers=headers, data=json_data)
        print(res.reason, flush=True)
        return res.status_code

@api.route('/event/callback')  # url pattern으로 name 설정
class EventCallback(Resource):
    def get(self):  
        return {"message" : "Welcome, EventCallback"}, 200

    def post(self):  
        #type_header = request.headers.get('Content-type')
        #url = request.json.get('targetURL')
        #api = request.json.get('API')

        data = request.get_json()
        #print(json.dumps(data))
        #res = json.dumps(data)

        return data, 200

if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0', port=8000)
    app.run(debug=True, host='0.0.0.0', port=8080)
