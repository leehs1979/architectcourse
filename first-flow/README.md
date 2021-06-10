## Flow Concept

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

