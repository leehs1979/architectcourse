from flask import Flask, request, jsonify
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
import flask_restful
from flask_restx import Resource, Api
import requests,json
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
api = Api(app)

@api.route('/')
class FlowInitiator(Resource):
    
    # POST 사용한다.
    def post(self):
        
        print('[START] FlowInitiator')
        
        req_data = request.get_json()
        print(req_data)
        
        #flowmanager_uri도 줄것
        # TODO: 변경할 것
        '''
        req_data = request.get_json()
        targetURL = req_data['targetURL']
        targetAPI = req_data['targetAPI']
        headers = req_data['headers']
        body = req_data['body']
        print(targetURL)
        print(targetAPI)
        print(headers)
        print(body)
        json_data=json.dumps(body)

        res = requests.post(targetURL+targetAPI, headers=headers, data=json_data)
        
        return res.json()
        '''
        
        print('[END] FlowInitiator')
        
        return 200
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=17000)