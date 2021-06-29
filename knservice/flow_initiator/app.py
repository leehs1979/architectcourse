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
        
        # input: 사용자 요청(시스템) -원래 # TODO: 하드코딩으로 몇개 만들어 두자. # http://172.16.1.110:17000/<id> 로 호출
        # flow_nm -> flow_id로 매핑
        # in_data
        # run_job_id
        # final_result_callback        
        '''
        1. 테스트 - sync1 - sync2 - async1 - sync3 : 결과 - OK

        {
            "flow_id": "a138634c-29d1-43cb-9e41-99dbc911e777",
            "in_data": { "type": 1 },
            "api_seq": 0,
            "run_job_id": "test1_runtime",
            "final_result_callback": "http://172.16.1.110:19000/callback_post",
            "service_dispatcher_uri": "http://172.16.1.110:18081",
            "service_async_receiver_uri": "http://172.16.1.110:18082"
        }


        2. 테스트 - sync1 - sync2 - sync3 : 결과 - OK

        {
            "flow_id": "0af0714b-5896-4894-b0ce-ab02ac570608",
            "in_data": { "type": 1 },
            "api_seq": 0,
            "run_job_id": "test2_runtime",
            "final_result_callback": "http://172.16.1.110:19000/callback_post",
            "service_dispatcher_uri": "http://172.16.1.110:18081",
            "service_async_receiver_uri": "http://172.16.1.110:18082"
        }
        '''
        
        # TODO: 위의 데이터로 1, 2, 3 등으로 나누어서 (post) service_dispatcher_uri로 호출하는 부분 만들기
        
        
        
        
        print('[END] FlowInitiator')
        
        return 200
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=17000)