# Knative - Sync Service

- 지원 API
```
"/": "POST",    
```
- 실행 : Pod 테스트
```
POST http://34.64.156.25:18081
{
    "flow_id": "602bbc33-f56e-41b5-9a88-596fb724021f",
    "in_data": 1,   
    "api_seq": 0,
    "run_job_id": "test_runtime_pod_0802_24",
    "final_result_callback": "http://34.64.134.132:19000/callback_post",                    
    "service_dispatcher_uri": "http://34.64.156.25:18081",
    "service_dispatcher_host": "svc-sender.flowmanager.example.com",
    "service_async_receiver_uri": "http://34.64.121.115:18082",                           
    "service_async_receiver_host": "svc-receiver.flowmanager.example.com",
    "is_pod_test": "Y"               
}

```
- 실행 : Knative 테스트
```
POST http://34.64.137.107/
Host: svc-dispatcher.flowmanager.example.com

{
    "flow_id": "ffdc78be-beb5-495c-8a1b-16f41bca9dfa",
    "in_data": 1,   
    "api_seq": 0,
    "run_job_id": "test_runtime_0802_5",
    "final_result_callback": "http://34.64.134.132:19000/callback_post",                    
    "service_dispatcher_uri": "http://34.64.137.107",
    "service_dispatcher_host": "svc-sender.flowmanager.example.com",
    "service_async_receiver_uri": "http://34.64.137.10",                           
    "service_async_receiver_host": "svc-receiver.flowmanager.example.com",
    "is_pod_test": "N"               
}
```
