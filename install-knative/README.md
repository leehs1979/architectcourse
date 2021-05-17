공식 설치 가이드 참고

knative-serving  : v0.22.0
knative-eventing : v0.22.0
kafka-operator   : 0.16.2

##########
serving
##########
https://knative.dev/docs/install/install-serving-with-yaml/

version check
kubectl get namespace knative-serving -o 'go-template={{index .metadata.labels "serving.knative.dev/release"}}'


##########
serving
##########
https://knative.dev/docs/install/install-eventing-with-yaml/

version check
kubectl get namespace knative-eventing -o 'go-template={{index .metadata.labels "eventing.knative.dev/release"}}'


##########
kafka-operator
##########
strimzi/strimzi-kafka-operator/releases/download/0.16.2
