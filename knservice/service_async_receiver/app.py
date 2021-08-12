from flask import Flask, request, jsonify
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
import flask_restful
from flask_restx import Resource, Api
import requests,json
from datetime import datetime, timezone, timedelta
import os
import traceback

app = Flask(__name__)
api = Api(app)

@api.route('/')
class ServiceAsyncReceiver(Resource):
    
    def post(self):        
        
        try:
            print('[START] ASyncReceiver')
            
            #flowmanager_url = "http://127.0.0.1:28000/api/"
            
            flowmanager_url = os.environ.get('FLOWMANAGER', '')
            
            if flowmanager_url == "":
                print('[ERROR] There is no flowmanager_url')
                raise Exception('There is no flowmanager_url...Fail')
            
            # Step1 : callback 리턴 데이터 확인(json) http://service_ip:port/?<flow_job_id>
            # body json - 'result'를 키로 가정한다.
            # 'flow_job_id'가 callback uri에 포함되어 있다.
            
            #print(request.query_string.decode())
            #flow_job_id = request.query_string.decode()        
            
            #print(request.get_json())
            #service_result = request.get_json()['result']
            
            req_data = request.get_json()
            print(req_data)        
            
            flow_job_id = req_data['flow_job_id']
            service_result = req_data['result']            
            
            # Step2 : flowmanager flow_job 정보를 가져온다. by flow_job_id
            flow_job_uri = "flow_job/"+flow_job_id+"/"
            res = requests.get(flowmanager_url+flow_job_uri) 
            #print("status_code = ", res.status_code)
            res_data = res.json()
            print("flow_job result = ", res_data)        
            
            # Step3 : flowmanager에서 api_output에 저장된 다음 호출 정보 등의 payload를 가져온다.
            next_service_data = res_data['api_output']
            print("next_service_data = ", next_service_data)
            print("type(next_service_data) = ", type(next_service_data))
            
            # str -> json 형태로 변경 TODO: CHECK 2021.08.21
            next_service_data_dict = json.loads(next_service_data)
            
            print("next_service_data_dict = ", next_service_data_dict)
            print("type(next_service_data_dict) = ", type(next_service_data_dict))
            
            print("next_service_data_dict['check_job_id'] = ", next_service_data_dict['check_job_id'])
            # check_job STATUS가 TIMEOUT인지 확인
            check_job_id = next_service_data_dict['check_job_id']
            check_job_uri = "check_job/"
            
            print("check_job_uri = ", check_job_uri)
                                    
            res_check = requests.get(flowmanager_url+check_job_uri+check_job_id)
            print("res_check = ", res_check)            
            
            res_check_data = res_check.json()      
            print("res_check_data = ", res_check_data)
            print("type(res_check_data) = ", type(res_check_data))
            
            check_status = res_check_data['check_status']
            print("check_status = ", check_status)
            
            temp_api_status = 'SUCCESS'
            if check_status == 'TIMEOUT':
                # TODO: FAILURE 업데이트 필요 -> T/O되도 실행도록 수정
                # raise Exception('Service is timeout...Fail')
                temp_api_status = 'FAIL'
                
            print("temp_api_status = ", temp_api_status)

            # timeout 이전에 요청이 정상처리되면 check_job 해제 필요 - STATUS : STARTED, CANCEL, TIMEOUT
            payload = {                
                "check_status": "CANCEL",
                "check_end_dt": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f'),
                "checker_id": res_check_data['check_job_id'],
                "flow_job": flow_job_id
            }
            
            print("res_check_data['checker_id'] = ", res_check_data['check_job_id'])
            
            payload_json = json.dumps(payload)
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            check_job_uri = "check_job/"+check_job_id+"/"
            
            print("check_job_uri = ", check_job_uri)
            print("payload_json = ", payload_json)
            print("type(payload_json) = ", type(payload_json))
            
            res_check = requests.put(flowmanager_url+check_job_uri, headers=headers, data=payload_json)
            #res_check_data = res_check.json()        
                    
            # Step4 : flowmanager에 end 시간, SUCCESS/FAILURE 전송
            payload = {
                #"api_status": "SUCCESS",
                "api_status": temp_api_status,
                "api_end_dt": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f'),
                "flow_dtl": res_data['flow_dtl']                  
            }
            payload_json = json.dumps(payload)
            headers = {'Content-Type': 'application/json; charset=utf-8'}        
            
            res = requests.put(flowmanager_url+flow_job_uri, headers=headers, data=payload_json) 
            print("status_code = ", res.status_code)
            res_data = res.json()
            print("flow_job result = ", res_data)
            
            # Step5 : 응답 데이터를 api_in으로 재처리 from step3        
            next_service_data_dict['in_data'] = service_result
            
            # Step5 : SUCCESS 일 경우 Next Service 호출 : sync 로직과 동일
            #         (마지막 서비스이면 최종 결과값을 받을 final_result_callback으로 보내준다.)       
                
            next_service_uri = ""
            
            # 마지막 서비스이면 최종 결과값을 받을 callback으로 보내준다.
            if next_service_data_dict['is_last'] == 'Y':
                next_service_uri = next_service_data_dict['final_result_callback']
            else: 
                next_service_uri = next_service_data_dict['service_dispatcher_uri']
            
            print('next_service_data_dict[service_dispatcher_host] : ')
            print(next_service_data_dict['service_dispatcher_host'])
            
            next_service_data_json = json.dumps(next_service_data_dict)
            headers = {'Content-Type': 'application/json; charset=utf-8', 'Host': next_service_data_dict['service_dispatcher_host']}
            
            res = requests.post(next_service_uri, headers=headers, data=next_service_data_json)
            print("status_code = ", res.status_code)        
            
            print('[END] ASyncReceiver')
            return 200   
       
        except Exception as ex:
            print('Error Occured while processing : %s' % ex)
            print('[TRACE]', traceback.format_exc())
            return 500
            #return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=18082)