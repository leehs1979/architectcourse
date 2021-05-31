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
