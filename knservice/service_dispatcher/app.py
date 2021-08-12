from flask import Flask, request, jsonify
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
import flask_restful
from flask_restx import Resource, Api
import requests, json
from datetime import datetime, timezone, timedelta
import time, os
import traceback

app = Flask(__name__)
api = Api(app)

@api.route('/')
class ServiceDispatcher(Resource):
    
    # POST 사용한다.
    def post(self):       
        
        try:
            print('[START] ServiceDispatcher')
            
            #flowmanager_url = "http://127.0.0.1:28000/api/"
                        
            flowmanager_url = os.environ.get('FLOWMANAGER', '')
            
            if flowmanager_url == "":
                print('[ERROR] There is no flowmanager_url')
                raise Exception('There is no flowmanager_url...Fail')
                        
            # Step1 : Flow_id 및 데이터 확인(json)
            # 예: a138634c-29d1-43cb-9e41-99dbc911e777
            req_data = request.get_json()
            print(req_data)        
            
            
            # initiator에서 최초 넘어오는 데이터 : 예시
            '''
            {
                "flow_id": "0af0714b-5896-4894-b0ce-ab02ac570608",
                "in_data": 1,   # async sleep time
                "api_seq": 0,
                "run_job_id": "test2_runtime",
                "final_result_callback": "http://IP:PORT/callback_post",                    # Callback for 일반 POD TEST if is_pod_test = 'Y'
                "service_dispatcher_uri": "http://IP:PORT",
                "service_dispatcher_host": "Host: svc-sender.flowmanager.example.com",
                "service_async_receiver_uri": "http://IP:PORT"                              # Callback for Knative TEST if is_pod_test = 'N'
                "service_async_receiver_host": "Host: svc-receiver.flowmanager.example.com",
                "is_pod_test": "N",                
            }
            '''
            
            flow_id = req_data['flow_id']
            in_data = req_data['in_data']   # object
            api_seq = req_data['api_seq']   # 1, 2, 3 순서를 가정한다.
            run_job_id = req_data['run_job_id']   # runtime id
            final_result_callback = req_data['final_result_callback']
            
            service_dispatcher_uri = req_data['service_dispatcher_uri']
            service_dispatcher_host = req_data['service_dispatcher_host']
            service_async_receiver_uri = req_data['service_async_receiver_uri']
            service_async_receiver_host = req_data['service_async_receiver_host']
            
            is_pod_test = req_data['is_pod_test']
            
            #print('flow_id:'+flow_id)
            
            # Step2 : flow 구성 flow_dtl 가져오기
            flow_dtl_uri = "flow_dtl/?flow="+flow_id
            flow_dtl_result = requests.get(flowmanager_url+flow_dtl_uri).json()
            #print('flow_dtl_result:', flow_dtl_result)
            
            # Step3 : flow_dtl에서 어느 부분(api_seq)인지 확인
            # initiator에서 처음에 오면 api_seq == 0, api_seq가 1이 되어야 함
            # Next Service 호출시 있으면(is_last) api_seq 붙임, 현재+1
            if api_seq == 0:
                print("Call by flow_initiator")
                api_seq = api_seq + 1       # current sequence
            
            service = {} 
            service['run_job_id'] = run_job_id
            
            for dtl in flow_dtl_result:
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

                # Step 5-1: TODO: in_data 준비 (사용자가 api를 읽어서 맞춰 보낸다고 가정한다.)
                # service['api_in_format'] : json 형태의 사용자 데이터이다.
                
                
                #Step 5-2: (1) service 호출(POST)
                #          (2) timeout 설정, retry 만큼 시도
                
                # retry 구현
                retry_count = 0
                for retry_count in range(service['api_retry']):           
                    
                    service_res = requests.get(service['api_uri'])
                    print("service status_code = ", service_res.json()) # json 형태의 리턴을 가정한다.
                    service_res_data = service_res.json()
                    
                    # print if status code is less than 400
                    print(service_res.ok)
                    if service_res.ok:
                        break
                    else:    
                        time.sleep(1)   # 1초 후 호출
                
                print("retry_count : ", retry_count)
                if retry_count + 1 == service['api_retry']:
                    raise Exception('Sync Service is not responsed...Fail')            
                
                '''
                # GET : OK
                service_res = requests.get(service['api_uri'])
                print("service status_code = ", service_res.json()) # json 형태의 리턴을 가정한다.
                service_res_data = service_res.json()
                '''
                
                # TODO: POST : POST Call로 가정한다.
                '''
                temp_in_data = {
                    "type": 1                
                }
                payload_json = json.dumps(temp_in_data)
                headers = {'Content-Type': 'application/json; charset=utf-8'}            
                            
                service_res = requests.post(service['api_uri'], headers=headers, data=payload_json)
                print("service status_code = ", service_res.status_code)
                service_res_data = service_res.json()
                print("service flow_job result = ", service_res_data)
                '''
                            
                #Step 5-3: flowmanager에 start 시간 전송 - flow_job 생성(json format)
                # "api_input": "{ type:1 }",
                # "api_status": "STARTED",
                # "api_start_dt": "2021-06-28T14:09:00Z", (현재시간) datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')
                # "run_job_id": "TestFlow_RUNTIME", service['run_job_id']
                # "creator": "Team2",
                # "flow_dtl": "Leehs", service['flow_dtl_id']
                # 오류 처리는 나중에 정상일 경우 201 리턴됨
                
                print("service['flow_dtl_id'] : ", service['flow_dtl_id'])
                print("in_data : ", in_data)
                
                payload = {
                    "api_input": in_data,
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
                print("status_code = ", res.status_code)
                res_data = res.json()
                print("flow_job result = ", res_data)
                
                flow_job_id = res_data['flow_job_id']
                
                # 정상 호출 후에 timeout 설정
                payload = {                
                    "check_status": "STARTED",
                    "check_start_dt": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f'),
                    "checker_id": service['run_job_id'],
                    "creator": "Team2",
                    "flow_job": flow_job_id,
                    "timeout": service['api_timeout']
                }
                payload_json = json.dumps(payload)
                headers = {'Content-Type': 'application/json; charset=utf-8'}
                check_job_uri = "check_job/"
                
                res = requests.post(flowmanager_url+check_job_uri, headers=headers, data=payload_json)
                res_data = res.json()
                check_job_id = res_data['check_job_id']      
                            
                #Step 5-4: service 호출(POST) 응답확인
                #json 형태의 리턴에서 'result'를 결과값으로 가정한다.
                next_in_data = service_res_data['result']
                
                # check_job STATUS가 TIMEOUT인지 확인
                res = requests.get(flowmanager_url+check_job_uri+check_job_id)
                res_data = res.json()      
                check_status = res_data['check_status']
                
                if check_status == 'TIMEOUT':
                    # TODO: FAILURE 업데이트 필요
                    raise Exception('Service is timeout...Fail')
                
                # timeout 이전에 요청이 정상처리되면 check_job 해제 필요 - STATUS : STARTED, CANCEL, TIMEOUT
                payload = {                
                    "check_status": "CANCEL",
                    "check_end_dt": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f'),
                    "checker_id": service['run_job_id'],
                    "flow_job": flow_job_id
                }
                
                payload_json = json.dumps(payload)
                headers = {'Content-Type': 'application/json; charset=utf-8'}
                check_job_uri = "check_job/"+check_job_id+"/"
                
                res = requests.put(flowmanager_url+check_job_uri, headers=headers, data=payload_json)
                res_data = res.json()
                
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
                    "flow_id": "0af0714b-5896-4894-b0ce-ab02ac570608",
                    "in_data": { "type": 1 },
                    "api_seq": 0,
                    "run_job_id": "test2_runtime",
                    "final_result_callback": "http://IP:PORT/callback_post",
                    "service_dispatcher_uri": "http://IP:PORT",
                    "service_dispatcher_host": "svc-sender.flowmanager.example.com",
                    "service_async_receiver_uri": "http://IP:PORT"
                    "service_async_receiver_host": "svc-receiver.flowmanager.example.com",
                    "is_pod_test": "N"
                }
                '''
                # Next Service 호출이 있으면(is_last='N') api_seq = api_seq+1
                # 응답 데이터를 api_in으로 재처리하여 전달
                # ksvc uri를 호출해야 한다.
                # async의 경우 api_out에 이 정보를 임시저장하고 Receiver에서 사용한다.
                            
                out_data = next_in_data   # API 호출 결과            
                
                next_service_data = {
                    "flow_id": flow_id,
                    #"in_data": out_data,
                    "in_data": in_data,     # 임시수정
                    "api_seq": api_seq + 1,
                    "run_job_id": run_job_id,
                    "final_result_callback": final_result_callback,
                    "service_dispatcher_uri": service_dispatcher_uri,
                    "service_dispatcher_host": service_dispatcher_host,
                    "service_async_receiver_uri": service_async_receiver_uri,
                    "service_async_receiver_host": service_async_receiver_host,
                    "is_pod_test": is_pod_test
                }
                
                print("next_service_data = ", next_service_data)
                
                next_service_uri = ""
                
                # 마지막 서비스이면 최종 결과값을 받을 callback으로 보내준다.
                if service['is_last'] == 'Y':
                    next_service_uri = final_result_callback
                else: 
                    next_service_uri = service_dispatcher_uri
                
                next_service_data_json = json.dumps(next_service_data)
                headers = {'Content-Type': 'application/json; charset=utf-8', 'Host': service_dispatcher_host}
                
                res = requests.post(next_service_uri, headers=headers, data=next_service_data_json)
                print("status_code = ", res.status_code)
                
            else:                               # async sender
                print("[START] Async Logic")
                # Step 5-1: in_data 준비 (사용자가 api를 읽어서 맞춰 보낸다고 가정한다.)
                # service['api_in_format'] : json 형태의 사용자 데이터이다.
                # TODO: 후순위            
                                                
                # Step 5-2: flowmanager에 flow_job을 생성한다. - start 시간 전송
                # flowmanager flow_job의 api_output에 다음 호출 정보 등의 payload 부분을 저장한다.(먼저 수행)
                '''
                next_service_data = {
                    "flow_id": flow_id,
                    "in_data": "1",                      # async_receiver에서 설정한다.(비동기 응답 받아야 한다.)
                    "api_seq": api_seq + 1,
                    "run_job_id": run_job_id,
                    "final_result_callback": final_result_callback,
                    "service_dispatcher_uri": service_dispatcher_uri,
                    "service_dispatcher_host": service_dispatcher_host,
                    "service_async_receiver_uri": service_async_receiver_uri,
                    "service_async_receiver_host": service_async_receiver_host,
                    "is_last": service['is_last']       # async_receiver에서 사용한다.(현재꺼, 다음 서비스 호출여부)
                }
                '''
                
                payload = {
                    "api_input": in_data,
                    "api_output": "",    # receiver에서 사용해야 한다.
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
                print("status_code = ", res.status_code)
                res_data = res.json()
                print("flow_job result = ", res_data)
                
                flow_job_id = res_data['flow_job_id']
                
                # Step 5-3: (1) service 호출(POST)
                #           (2) timeout 설정, retry 만큼 시도
                
                # 대상 서비스 호출은 POST, 비동기이므로 바로 response가 온다. 
                # 서비스 호출 시에 callback uri(ASyncReceiver)에 flow_job_id를 붙여서 보낸다.
                #      "callback" : "http://service_ip:port/<flow_job_id>" 가 리턴받을 callback_uri이다.(이대로 달라고 한다.)

                callback_uri = ""
                target_uri = ""
                headers = {}
                callback_uri = service_async_receiver_uri+"/?"+flow_job_id
                
                if is_pod_test != 'Y':                    
                    
                    #CloudEvent Header
                    #headers = {
                    #    'Ce-specversion': '0.3',
                    #    'Ce-Type': 'dev.knative.samples.t2',
                    #    'Ce-Source': 'dev.knative.samples/t2',
                    #    'Content-Type': 'application/json'
                    #}
                    headers['Ce-specversion']='0.3'
                    headers['Ce-Type']='dev.knative.samples.t2'
                    headers['Ce-Source']='dev.knative.samples/t2'
                    headers['Content-Type']='application/json'
                    headers['Ce-Id']=flow_job_id # flow 에서 사용하는 id 로 써도 되는지 확인 필요 '536808d3-88be-4077-9d7a-a3f162705f79'
                                        
                    api_in_body = {
                        "api_input": in_data,           # TODO: 데이터 처리필요
                        "callback" : callback_uri
                    }
                    
                    # external api 의 url, header, body 부분이 cloudevent body 로 설정
                    api_in_data = {
                        "api_uri" : service['api_uri'],
                        "headers" : headers,
                        "body" : api_in_body
                    }
                    
                    target_uri = "http://broker-ingress.knative-eventing.svc.cluster.local/default/kafka-backed-broker"
                    
                else:                    
                    
                    api_in_data = {
                        "api_input": in_data,      # TODO: 데이터 처리필요
                        "callback" : callback_uri
                    }
                    
                    #headers = {'Content-Type': 'application/json; charset=utf-8'}
                    headers['Content-Type'] = 'application/json; charset=utf-8'                    
                    target_uri = service['api_uri']
                    
                print("callback_uri : ", callback_uri)                
                api_in_data_json = json.dumps(api_in_data)                 
                print("api_in_data_json : ", api_in_data_json)
                
                # retry 구현
                retry_count = 0
                for retry_count in range(service['api_retry']):           
                    
                    #service_res = requests.post(service['api_uri'], headers=headers, data=api_in_data_json)
                    service_res = requests.post(target_uri, headers=headers, data=api_in_data_json)
                    print("service status_code = ", service_res.status_code)    # 201 will return
                    
                    # print if status code is less than 400
                    print(service_res.ok)
                    if service_res.ok:
                        break
                    else:    
                        time.sleep(1)   # 1초 후 호출
                
                print("retry_count : ", retry_count)
                if retry_count + 1 == service['api_retry']:
                    raise Exception('Async Service is not responsed...Fail')
                
                # 정상 호출 후에 timeout 설정
                payload = {                
                    "check_status": "STARTED",
                    "check_start_dt": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f'),
                    "checker_id": service['run_job_id'],
                    "creator": "Team2",
                    "flow_job": flow_job_id,
                    "timeout": service['api_timeout']
                }
                payload_json = json.dumps(payload)
                headers = {'Content-Type': 'application/json; charset=utf-8'}
                check_job_uri = "check_job/"
                
                res = requests.post(flowmanager_url+check_job_uri, headers=headers, data=payload_json)
                res_data = res.json()
                check_job_id = res_data['check_job_id']
                
                # 다음 서비스를 준비한다. (check_job_id 추가한다. - Receiverd에서 Timeout 처리목적)
                next_service_data = {
                    "flow_id": flow_id,
                    "in_data": "",                      # async_receiver에서 설정한다.(비동기 응답 받아야 한다.)
                    "api_seq": api_seq + 1,
                    "run_job_id": run_job_id,
                    "final_result_callback": final_result_callback,
                    "service_dispatcher_uri": service_dispatcher_uri,
                    "service_dispatcher_host": service_dispatcher_host,
                    "service_async_receiver_uri": service_async_receiver_uri,
                    "service_async_receiver_host": service_async_receiver_host,
                    "is_last": service['is_last'],      # async_receiver에서 사용한다.(현재꺼, 다음 서비스 호출여부)
                    "check_job_id": check_job_id,       # async_receiver에서 사용한다.(현재꺼, timeout check)
                    "is_pod_test": is_pod_test
                }
                
                payload = {
                    "api_output": json.dumps(next_service_data),                
                    "flow_dtl": service['flow_dtl_id']
                }
                
                payload_json = json.dumps(payload)
                headers = {'Content-Type': 'application/json; charset=utf-8', 'Host': service_async_receiver_host}
                flow_job_uri = "flow_job/"+flow_job_id+"/"
                
                res = requests.put(flowmanager_url+flow_job_uri, headers=headers, data=payload_json)
                
                # 다음 서비스 호출없이 종료한다.
                print("[END]] Async Logic")
            
            print('[END] ServiceDispatcher')
            
            return 200
        
        except Exception as ex:
            print('Error Occured while processing : %s' % ex)
            print('[TRACE]', traceback.format_exc())                   
            return 500
            #return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=18081)