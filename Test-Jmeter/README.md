## Server 접속
- team2-jmeter1 서버에 SSH 접속
- root 계정으로 변경

## Script 변경
- 위치 : /root/apache-jmeter-5.4.1/bin/script
- POD 용 : pod.jmx
- knative 용 : knative.jmx

## 수정 필요 내용
- run_job_id 관련 

```
<elementProp name="TC_NUM" elementType="Argument"> 아래       
<stringProp name="Argument.value">1</stringProp> => TC 번호를 지정하여 다른 테스트와 구분되도록 해야 함

test_runtime_pod_${__time(MMdd)}_TC_${TC_NUM}_${__threadNum} => 날짜자동 생성되도록 함(별도 수정 불필요)
```

- thread 갯수 관련

```
<stringProp name="ThreadGroup.num_threads">100</stringProp> => 동시 수행할 thread 갯수
```

- 그 외 수정 필요 부분은 차차 수정 필요

## 수행 명령어
- cd /root/apache-jmeter-5.4.1/bin
- POD 용 : ./jmeter.sh -n -t script/pod.jmx -l test_pod.log
- knative 용 : ./jmeter.sh -n -t script/knative.jmx -l test.log
