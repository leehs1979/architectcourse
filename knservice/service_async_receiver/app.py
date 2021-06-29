from flask import Flask, request, jsonify
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
import flask_restful
from flask_restx import Resource, Api
import requests,json

app = Flask(__name__)
api = Api(app)

@api.route('/')
class ServiceAsyncReceiver(Resource):
    
    def post(self):
        
        print('TEST ASyncReceiver')
        
        # TODO: Step1 : callback 리턴 데이터 확인(json) http://service_ip:port/<flow_job_id>
        # body json - 'result'를 키로 가정한다.
        # 'flow_job_id'가 callback uri에 포함되어 있다.
        
        # TODO: Step2 : flowmanager에 end 시간, SUCCESS/FAILURE 전송
        
        # TODO: Step3 : flowmanager에서 api_output에 저장된 다음 호출 정보 등의 payload를 가져온다.
        
        # TODO: Step4 : 응답 데이터를 api_in으로 재처리
        
        # TODO: Step5 : SUCCESS 일 경우 Next Service 호출 : sync 로직과 동일
        #               (마지막 서비스이면 최종 결과값을 받을 final_result_callback으로 보내준다.)
        
        return 200   
    
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=18083)