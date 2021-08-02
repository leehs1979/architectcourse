
### knative scale 설정

참고 URL : https://docs.openshift.com/container-platform/4.3/serverless/knative_serving/configuring-knative-serving-autoscaling.html

```
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "10"
```
