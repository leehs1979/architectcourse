# Flowmanager

Django Rest framework 사용
- 기본적으로 Rest API(CRUD)와 간단한 UI 페이지를 제공함
- 접속 URL : [http://35.227.165.228:8000/api/](http://35.227.165.228:8000/api/)
- 지원 API
```
    "flow": "http://35.227.165.228:8000/api/flow",    
    "flow_dtl": "http://35.227.165.228:8000/api/flow_dtl/",
    "api": "http://35.227.165.228:8000/api/api/",
    "flow_job": "http://35.227.165.228:8000/api/flow_job/",
    
    "schedule": "http://35.227.165.228:8000/api/flow/schedule/",
    "user": "http://35.227.165.228:8000/api/user/"
```
- 실행
```sh
$ docker-compose up -d --build
```


# Kubernetes 환경
- Postgresql 접속정보
```
namespace : flowmanager
service : postgres
접속정보 :
   name: POSTGRES_DB
   value: mydb
   name: POSTGRES_USER
   value: team2
   name: POSTGRES_PASSWORD
   value: team2		
   ports:
    - containerPort: 5432
        
```
