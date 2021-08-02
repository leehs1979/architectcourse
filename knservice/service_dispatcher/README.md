# Knative - Sync Service

- 지원 API
```
"/": "POST",    
```
- 실행
```

curl -v http://34.64.137.107/ \
-X POST \
-H "Host: svc-dispatcher.flowmanager.example.com" \
-H "Content-Type: application/json" \
-d \
'{
    "flow_id": "ffdc78be-beb5-495c-8a1b-16f41bca9dfa",
    "in_data": { "type": 1 },
    "api_seq": 0,
    "run_job_id": "test_runtime_0802_1",
    "final_result_callback": "http://34.64.134.132:19000/callback_post",
    "service_dispatcher_uri": "http://34.64.137.107/",
	"service_dispatcher_host": "svc-dispatcher.flowmanager.example.com",
    "service_async_receiver_uri": "http://34.64.137.107/",
	"service_async_receiver_host": "svc-async-receiver.flowmanager.example.com"
}'
```

