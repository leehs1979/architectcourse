## Flow Concept(2021.06.16)
- Sync : curl(VM) -> Send serving(K8S) -> API Sample(http://34.64.132.164:30000)
- ASync : curl(VM) -> Send serving(K8S) -> Broker -> Receive Serving -> API Sample(http://34.64.132.164:30000)

## 1. ./send-cloudevents/send-serving.yml
- 기존의 send-cloudevents 를 확장하여 Knative Serving 으로 제공
```
kubectl get ksvc send-serving 명령어로 배포 결과 확인 가능
NAME                         URL                                                     LATESTCREATED                      LATESTREADY                        READY   REASON
send-serving                 http://send-serving.default.example.com                 send-serving-00001                 send-serving-00001                 True
=> 특이사항 default 로 배포시 serving 에서는 http 8080 포트 체크를 함
=> python 이 8080 으로 서비스하지 않는다면 설정 변경 필요
```

- knative serving 으로 제공시 istio ingress gateway를 통하여 호출이 되어야 함
```
jhyun82_choi@cloudshell:~$ kubectl get svc istio-ingressgateway -n istio-system
NAME                   TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)                                                                      AGE
istio-ingressgateway   LoadBalancer   10.100.35.96   34.64.137.107   15021:31864/TCP,80:32151/TCP,443:31539/TCP,15012:32215/TCP,15443:32023/TCP   2d21h
```

## 2. ./send-cloudevents/app.py
- 콘솔 접속하여 아래와 같이 호출 가능
- GET /sync API
```
curl -v http://34.64.137.107/sync \
-X GET \
-H "Host: send-serving.default.example.com" \
-H "Content-Type: application/json" \
-d @./get_sync_tasks.json

get_sync_tasks.json 내용
{
    "targetURL" : "http://34.64.132.164:30000",
    "targetAPI" : "/sync_tasks/abcdevflake",
    "headers" : {
        "Content-type" : "application/json",
        "Header1" : "Header1",
        "Header2" : "Header2"
    },
    "body" : {
        "callback-url" : "http://send-cloudevent:8000",
        "callback-api" : "/event/callback",
        "parameter2" : "parameter2",
        "parameter3" : "parameter3"
    }
}
```
- POST /sync
```
ex)
 curl -v http://34.64.137.107/sync \
-X POST \
-H "Host: send-serving.default.example.com" \
-H "Content-Type: application/json" \
-d @./post_sync_tasks.json

post_sync_tasks.json 내용
{
    "targetURL" : "http://34.64.132.164:30000",
    "targetAPI" : "/tasks",
    "headers" : {
        "Content-type" : "application/json",
        "Header1" : "Header1",
        "Header2" : "Header2"
    },
    "body" : {
        "type" : "10"
    }
}
```

- POST /async
```
curl -v http://34.64.137.107/async \
-X POST \
-H "Host: send-serving.default.example.com" \
-H "Content-Type: application/json" \
-d @./post_async_tasks.json

post_async_tasks.json 내용
{
    "targetURL" : "http://34.64.132.164:30000",
    "targetAPI" : "/callback_tasks",
    "headers" : {
        "Content-type" : "application/json",
        "Header1" : "Header1",
        "Header2" : "Header2"
    },
    "body" : {
        "callback_uri" : "http://34.64.137.107/event/callback",
        "host" : "send-serving.default.example.com"
    }
}
```
- POST /event/callback
```
호출시 header 값에 host 로 전달된 send-serving.default.example.com 값이 설정되어 있어야 함
curl -v http://34.64.137.107/event/callback \
-X POST \
-H "Host: send-serving.default.example.com" \
-H "Content-Type: application/json" \
-d @./post_async_tasks.json
```
========================================================================================================================================================
## Flow Concept(before 2021.06.15)

curl -> Send cloud event -> Broker -> Receive cloud event -> External

## 1. send-cloudevents

외부에서 이벤트를 발생시키기 위한 api 를 제공한다.
K8S 의 Service(Loadbalancer) 와 deployment 로 구성되며 Broker 에게 post 요청을 통하여 이벤트를 전달한다.

/event : Broker 에 이벤트를 전달하기 위한 POST Method

/event/callback: callback 처리를 위함 임시 GET/POST Method

ex) 
curl -X POST http://send-cloudevent:8000/event -H "Content-type:application/json" -d '{"targetURL" : "http://35.226.56.118", "targetAPI" : "/test", "headers":"headers", "body":"body"}' 
(코드상 headers, body 는 필요하다. 없으면 receive cloudevent 에서 500 에러 발생)

## 2. receive-cloudevents

Broker 를 구독하고 있으며 Trigger 에 의해 이벤트를 전달 받아 CloudEvent Type 을 Json 으로 변환하여 외부 api 서버를 호출하도록 한다. Knative Serving 으로 제공


## 결과
이벤트 발생 - 클러스터 접속 가능한 IP 가 없어 클러스터내에 임의로 접속
```
root@send-cloudevent-5fc754445c-sgcl8:/app# curl -X POST http://localhost:8000/event -H "Content-type:application/json" -d @./test.json
202
root@send-cloudevent-5fc754445c-sgcl8:/app# curl -X POST http://localhost:8000/event -H "Content-type:application/json" -d @./test.json
202

test.json 
{
    "targetURL" : "http://35.226.56.118", 
    "targetAPI" : "/test",
    "headers" : {
        "Content-type" : "application/json",
        "Header1" : "Header1",
        "Header2" : "Header2"
    },
    "body" : {
        "callback-url" : "http://send-cloudevent:8000",
        "callback-api" : "/event/callback",
        "parameter2" : "parameter2",
        "parameter3" : "parameter3"
    }
}
```

## 이벤트 확인
kubectl logs broker-kafka-display-00001-deployment-6b486d7dc5-2kqqb -c user-container -f
```
☁️  cloudevents.Event
Validation: valid
Context Attributes,
  specversion: 0.3
  type: dev.knative.samples.t2
  source: dev.knative.samples/t2
  id: 536808d3-88be-4077-9d7a-a3f162705f79
  datacontenttype: application/json
Extensions,
  knativearrivaltime: 2021-05-18T04:10:04.347635944Z
Data,
  {
    "targetURL": "http://35.226.56.118",
    "targetAPI": "/test",
    "headers": {
      "Content-type": "application/json",
      "Header1": "Header1",
      "Header2": "Header2"
    },
    "body": {
      "callback-url": "http://send-cloudevent:8000",
      "callback-api": "/event/callback",
      "parameter2": "parameter2",
      "parameter3": "parameter3"
    }
  }
```

## 이벤트 처리(serving)
```
[root@architect21-team2-master first-flow]# kubectl get pod
NAME                                                     READY   STATUS    RESTARTS   AGE
broker-kafka-display-00001-deployment-6b486d7dc5-2kqqb   2/2     Running   0          5d4h
curl                                                     1/1     Running   0          21h
hello-world-7677cdf8dd-6rrv7                             1/1     Running   0          7d1h
hello-world-7677cdf8dd-7llcl                             1/1     Running   0          7d1h
hello-world-7677cdf8dd-b49tm                             1/1     Running   0          7d1h
hello-world-7677cdf8dd-dgpkl                             1/1     Running   0          7d1h
hello-world-7677cdf8dd-p8p8m                             1/1     Running   0          7d1h
send-cloudevent-5fc754445c-sgcl8                         1/1     Running   0          108m
[root@architect21-team2-master first-flow]# 
[root@architect21-team2-master first-flow]# 
[root@architect21-team2-master first-flow]# 
[root@architect21-team2-master send-cloudevents]# kubectl get pod
NAME                                                           READY   STATUS    RESTARTS   AGE
broker-kafka-display-00001-deployment-6b486d7dc5-2kqqb         2/2     Running   0          5d4h
curl                                                           1/1     Running   0          21h
hello-world-7677cdf8dd-6rrv7                                   1/1     Running   0          7d1h
hello-world-7677cdf8dd-7llcl                                   1/1     Running   0          7d1h
hello-world-7677cdf8dd-b49tm                                   1/1     Running   0          7d1h
hello-world-7677cdf8dd-dgpkl                                   1/1     Running   0          7d1h
hello-world-7677cdf8dd-p8p8m                                   1/1     Running   0          7d1h
receive-cloudevent-service-00001-deployment-6b589b76bb-f7jrv   2/2     Running   0          12s
send-cloudevent-5fc754445c-sgcl8                               1/1     Running   0          113m
```

