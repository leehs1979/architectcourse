## Server 접속
- team2-jmeter1 서버에 SSH 접속
- root 계정으로 변경

## Script 변경
- 위치 : /root/apache-jmeter-5.4.1/bin/script
- POD 용 : pod.jmx
- knative 용 : knative.jmx

## 수정 필요 내용
- run_job_id 관련 
: "<stringProp name="Argument.value">1</stringProp>" => 1 을 변경하여 TC 번호를 변경 

- thread 갯수 관련
: <stringProp name="ThreadGroup.num_threads">100</stringProp> => 동시 수행할 thread 갯수

- 그 외 수정 필요 부분은 차차 수정 필요

## 수행 명령어
- cd /root/apache-jmeter-5.4.1/bin
- POD 용 : ./jmeter.sh -n -t script/pod.jmx -l test_pod.log
- knative 용 : ./jmeter.sh -n -t script/knative.jmx -l test.log
