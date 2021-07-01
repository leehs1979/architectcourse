# 외부 연계서비스 Sample

Async 요청을 받으면 202를 리턴하고 Callback과 ResultAPI(status endpoint)를 지원한다.

- 실행
```sh
$ docker-compose up -d --build
```

- 접속 URL
[http://35.227.165.228:5004/](http://35.227.165.228:5004)

- 지원 API : 동기서비스, 비동기서비스 지원
```
- Flask (서버) : 5004
  . URI1 : /tasks
	- 요청(IN) : post {"type" : 10 } => Sleep 시간
	- 리턴(OUT): 202, task_id
	- Test UI : http://35.227.165.228:5004/
  
  . URI2 : /tasks/<task_id>	- Client Polling 용도
	- 요청(IN) : get
	- 리턴(OUT): 200, task_result 객체(id, 상태, 결과)
	- 예) curl http://35.227.165.228:5004/tasks/99fe1ef7-2348-4b8c-aee5-f712b4e5e629
  
  . URI3 : /callback_tasks - 지정한 url로 리턴받는 용도
	- 요청(IN) : post callback_uri
	- 리턴(OUT): 200, task_id
	- 예) curl http://35.227.165.228:5004/callback_tasks/
	     post {"callback_uri" : "http://35.227.165.228:5008/callback" }	=> Sample Service
```

# Kubernetes 환경
- 설치 환경 및 접속    
  namespace : apisample

- 접속 URL
```  
  K8s 내부(service)  : curl web.apisample:5004
  K8s 외부(nodeport) : curl 34.64.132.164:30000      
```
- Test 동적 API
```

 URI4 : /sync_tasks/api_id
        - 용도 : 동기식 API sample
	- 로직 : 1초 sleep 후 응답  / api_id는 client에서 동적으로 전달 가능
	- 요청(IN) : get callback_uri
	- 리턴(OUT): 200, api_id (client가 던진)
	- 예) curl URI/sync_tasks/api11
	    


 URI5 : /callback_tasks/api_id	
        - 용도 : 비동기식 API sample
	- 로직 : 10초 sleep 후 응답  / api_id는 client에서 동적으로 전달 가능        
	- 요청(IN) : post callback_uri
	- 리턴(OUT): 200, task_id, api_id
	- 예) curl URI/callback_tasks/api_id
	     post {"callback_uri" : "http://www.naver.com" }	=> test Service

```
- Test Sample

sync Call
```
curl "web.apisample:5004/sync_tasks/sync1" -X GET
```
sync return
```
{
  "api_id": "sync1"
}
```

async call
```
curl "web.apisample:5004/callback_tasks/async1" \
-X POST \
-H "Content-Type: application/json" \
-d '{"callback_uri":"http://www.naver.com"}'
```

async return
```
{
  "api_id": "async1",
  "task_id": "46600c6e-e909-418a-ac3a-cecb348f0177"
}
```
