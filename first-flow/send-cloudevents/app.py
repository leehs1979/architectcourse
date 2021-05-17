from flask import Flask, request, jsonify
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
import flask_restful
from flask_restx import Resource, Api
from cloudevents.http import CloudEvent, to_structured
import requests

app = Flask(__name__)
api = Api(app)


@api.route('/event')  # url pattern으로 name 설정
class CreateEvent(Resource):
    def get(self):  
        return {"message" : "Welcome, Event"}
    def post(self):  
        type_header = request.headers.get('Content-type')
        url = request.json.get('targetURL')
        api = request.json.get('targetAPI')
        
        headers = {
            "Content-type" : "application/json"
        }
        # brocker 생성시 attribute 설정 없음
        attributes = {
                       "type": "com.example.sampletype2",
                        "source": "https://example.com/event-producer",
                    }
        datas = request.get_json()
        #data=request.json
        print(datas)

        # brocker 생성시 cloud event 사용하지 않음
        event = CloudEvent(attributes, datas)
        headers, body = to_structured(event)

        print(url)
        print(api)
        requests.post("http://172.17.0.4:8001", data=body, headers=headers) # 가상의 이벤트 발생 broker 주소
        #return jsonify({'targetURL' : url, 'targetAPI' : api})
        return jsonify(datas)

@api.route('/event/callback')  # url pattern으로 name 설정
class EventCallback(Resource):
    def get(self):  
        return {"message" : "Welcome, EventCallback"}

    def post(self):  
        #type_header = request.headers.get('Content-type')
        #url = request.json.get('targetURL')
        #api = request.json.get('API')

        body = jsonify(request.json)
        result = request.json.get('result')

        return jsonify({'result' : result})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
