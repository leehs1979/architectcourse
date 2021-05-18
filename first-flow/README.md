## Flow Concept

curl -> Send cloud event -> Broker -> Receive cloud event -> External

1. send-cloudevents
외부에서 이벤트를 발생시키기 위한 api 를 제공한다.
K8S 의 Service(Loadbalancer) 와 deployment 로 구성되며 Broker 에게 post 요청을 통하여 이벤트를 전달한다.

/event : Broker 에 이벤트를 전달하기 위한 POST Method
/event/callback: callback 처리를 위함 임시 GET/POST Method

ex) 
curl -X POST http://send-cloudevent:8000/event -H "Content-type:application/json" -d '{"targetURL" : "http://35.226.56.118", "targetAPI" : "/test"}'


2. receive-cloudevents
Broker 를 구독하고 있으며 Trigger 에 의해 이벤트를 전달 받아 CloudEvent Type 을 Json 으로 변환하여
외부 api 서버를 호출하도록 한다. Knative Serving 으로 제공
