from flask import Flask, request, jsonify
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
import flask_restful
from flask_restx import Resource, Api
import requests, json
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
api = Api(app)

@api.route('/')
class ServiceDispatcher(Resource):
    
    # POST 사용한다.
    def post(self):       
        
        print('TEST POST')
        
        flowmanager_url = "http://127.0.0.1:28000/api/"
        
        # Step1 : Flow_id 및 데이터 확인(json)
        # 예: a138634c-29d1-43cb-9e41-99dbc911e777
        req_data = request.get_json()
        print(req_data)        
        
        
        # initiator에서 최초 넘어오는 데이터
        '''
        {
            "flow_id": "a138634c-29d1-43cb-9e41-99dbc911e777",
            "in_data": {},
            "api_seq": 0,
            "run_job_id": "test1_runtime",
            "final_result_callback": "",
            "ksvc_uri": ""
        }
        '''
        
        flow_id = req_data['flow_id']
        in_data = req_data['in_data']   # object
        api_seq = req_data['api_seq']   # 1, 2, 3 순서를 가정한다.
        run_job_id = req_data['run_job_id']   # runtime id
        final_result_callback = req_data['final_result_callback']
        ksvc_uri = req_data['ksvc_uri']
        
        #print('flow_id:'+flow_id)
        
        # Step2 : flow 구성 flow_dtl 가져오기
        flow_dtl_uri = "flow_dtl/?flow="+flow_id
        flow_dtl_result = requests.get(flowmanager_url+flow_dtl_uri).json()
        #print('flow_dtl_result:', flow_dtl_result)
        
        # Step3 : flow_dtl에서 어느 부분(api_seq)인지 확인
        # initiator에서 처음에 오면 api_seq == 0, api_seq가 1이 되어야 함
        # Next Service 호출시 있으면(is_last) api_seq 붙임, 현재+1
        if api_seq == 0:
            print("Call by initiator")
            api_seq = api_seq + 1       # current sequence
        
        service = {} 
        service['run_job_id'] = run_job_id
        
        for dtl in flow_dtl_result:
            print(dtl['api_seq'], "--", api_seq)
            if dtl['api_seq'] == api_seq:
                service['flow_dtl_id'] = dtl['flow_dtl_id']
                service['api_timeout'] = dtl['api_timeout']
                service['api_retry'] = dtl['api_retry']
                service['is_last'] = dtl['is_last']
                service['api_id'] = dtl['api']
                break
        
        #print(service)
        
        # Step4 : 호출할 api 정보 가져오기 by api_id
        api_uri = "api/"+service['api_id']
        api_result = requests.get(flowmanager_url+api_uri).json()
                
        #print('api_result:', api_result)    
        
        # sync인지 async인지 여기서 알 수 있다. sync와 async_sender는 같이 사용 가능하다.
        service['api_type'] = api_result['api_type']       # sync / async
        service['api_uri'] = api_result['api_uri']
        service['api_in_format'] = api_result['api_in_format']
        
        #print(service)
                
        # Step5 : 구분하여 service 호출
        service_result = []
        if service['api_type'] == 'sync':   # sync

            # Step 5-1: in_data 준비 (사용자가 api를 읽어서 맞춰 보낸다고 가정한다.)
            # service['api_in_format'] : json 형태의 사용자 데이터이다.
            
            
            #Step 5-2: (1) service 호출(POST)
            #TODO:     (2) timeout 설정, retry 만큼 시도
            # api-sample 서비스 올려서 테스트 해보자 : 우선 로컬에서
            
            # GET : OK
            service_res = requests.get(service['api_uri'])
            print("service status_code = ", service_res.json()) # json 형태의 리턴을 가정한다.
            service_res_data = service_res.json()
            
            # POST : POST Call로 가정한다.
            '''
            temp_in_data = {
                "type": 1                
            }
            payload_json = json.dumps(temp_in_data)
            headers = {'Content-Type': 'application/json; charset=utf-8'}            
                        
            res = requests.post(service['api_uri'], headers=headers, data=payload_json)
            print("service status_code = ", res.status_code)
            res_data = res.json()
            print("service flow_job result = ", res_data)
            '''
                        
            #Step 5-3: flowmanager에 start 시간 전송 - flow_job 생성(json format)
            # "api_input": "{ type:1 }",
            # "api_status": "STARTED",
            # "api_start_dt": "2021-06-28T14:09:00Z", (현재시간) datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')
            # "run_job_id": "TestFlow_RUNTIME", service['run_job_id']
            # "creator": "Team2",
            # "flow_dtl": "Leehs", service['flow_dtl_id']
            # 오류 처리는 나중에 정상일 경우 201 리턴됨
            
            print("service['flow_dtl_id'] : "+service['flow_dtl_id'])
            
            payload = {
                "api_input": "{ type:1 }",
                "api_status": "STARTED",
                "api_start_dt": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f'),
                "run_job_id": service['run_job_id'],
                "creator": "Team2",
                "flow_dtl": service['flow_dtl_id']
            }
            payload_json = json.dumps(payload)
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            flow_job_uri = "flow_job/"
                        
            res = requests.post(flowmanager_url+flow_job_uri, headers=headers, data=payload_json)
            #print("status_code = ", res.status_code)
            res_data = res.json()
            #print("flow_job result = ", res_data)
            
            flow_job_id = res_data['flow_job_id']           
            
                        
            #Step 5-4: service 호출(POST) 응답확인
            #json 형태의 리턴에서 'result'를 결과값으로 가정한다.
            next_in_data = service_res_data['result']            
            
            #Step 5-5: flowmanager에 end 시간, SUCCESS/FAILURE 전송
            
            payload = {
                "api_status": "SUCCESS",
                "api_end_dt": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f'),
                "flow_dtl": service['flow_dtl_id']
            }
            
            #flow_job_id = "49c54560-8ae5-4752-b59c-0c51ab049895"
            
            payload_json = json.dumps(payload)
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            flow_job_uri = "flow_job/"+flow_job_id+"/"
            
            res = requests.put(flowmanager_url+flow_job_uri, headers=headers, data=payload_json)            
            
            #Step 5-6: SUCCESS 일 경우 Next Service 호출
            # 넘겨줘야 하는 데이터
            '''
            {
                "flow_id": "a138634c-29d1-43cb-9e41-99dbc911e777",
                "in_data": {},
                "api_seq": 0,
                "run_job_id": "test1_runtime",
                "final_result_callback": "",
                "ksvc_uri": ""
            }
            '''
            # Next Service 호출이 있으면(is_last='N') api_seq = api_seq+1
            # 응답 데이터를 api_in으로 재처리하여 전달
            # ksvc uri를 호출해야 한다.
            # async의 경우 api_out에 이 정보를 임시저장하고 Receiver에서 사용한다.
                        
            out_data = next_in_data   # API 호출 결과            
            
            payload = {
                "flow_id": flow_id,
                "in_data": out_data,
                "api_seq": api_seq + 1,
                "run_job_id": run_job_id,
                "final_result_callback": final_result_callback,     # 최종 callback 정해주고 테스트하자.
                "ksvc_uri": ksvc_uri
            }
            
            print(payload)
            
            next_service_uri = ""
            
            # 마지막 서비스이면 최종 결과값을 받을 callback으로 보내준다.
            if service['is_last'] == 'Y':
                next_service_uri = final_result_callback
            else: 
                next_service_uri = ksvc_uri
            
            payload_json = json.dumps(payload)
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            
            res = requests.post(next_service_uri, headers=headers, data=payload_json)
            print("status_code = ", res.status_code)
            
        else:                               # async sender
            print("async logic")
            #flow_job 생성 이전까지의 로직은 공유한다.
            
            #TODO: flowmanager에 flow_job을 생성한다.
            
            #TODO: 서비스 호출 시에 callback uri(ASyncReceiver)에 flow_job_id를 붙여서 보낸다.
            #      "callback" : "http://service_ip:port/<flow_job_id>" 가 리턴받을 callback_uri이다.(이대로 달라고 한다.)
            #TODO: Timeout, retry 등을 설정한다.
            
            #TODO: flowmanager flow_job의 api_output에 다음 호출 정보 등의 payload 부분을 저장한다.
            
            #다음 서비스 호출없이 종료한다.
        
        return 200
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=18081)