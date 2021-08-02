
### 참고 URL
https://www.kisphp.com/postgres/run-postgres11-and-pgadmin4-in-kubernetes-for-testing


### pvc
```
cat << EOF | kubectl apply -n flowmanager -f -
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: pgadmin
  labels:
    app: pgadmin
  annotations:
    volume.alpha.kubernetes.io/storage-class: default
spec:
  accessModes:
    - "ReadWriteOnce"
  resources:
    requests:
      storage: "5Gi"
EOF
```

### node port service
```
cat << EOF | kubectl apply -n flowmanager -f -
apiVersion: v1
kind: Service
metadata:
  name: pgadmin
  labels:
    app: pgadmin
spec:
  type: NodePort
  ports:
    - port: 80
      nodePort: 30002
  selector:
    app: pgadmin
EOF
```

### deployment

```
cat << EOF | kubectl apply -n flowmanager -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pgadmin
  labels:
    app: pgadmin
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pgadmin
  template:
    metadata:
      labels:
        app: pgadmin
    spec:
      initContainers:
        - name: pgadmin-data-permission-fix
          image: busybox
          command: ["/bin/chown", "-R", "5050:5050", "/var/lib/pgadmin"]
          volumeMounts:
          - name: pgadmin-data
            mountPath: /var/lib/pgadmin	
      containers:
        - name: pgadmin
          image: "dpage/pgadmin4"
          imagePullPolicy: IfNotPresent
          env:
            - name: PGADMIN_DEFAULT_PASSWORD
              value: team2
            - name: PGADMIN_DEFAULT_EMAIL
              value: team2@samsung.com
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
            - name: https
              containerPort: 443
              protocol: TCP
          volumeMounts:
            - name: pgadmin-data
              mountPath: /var/lib/pgadmin
      volumes:
        - name: pgadmin-data
          persistentVolumeClaim:
            claimName: pgadmin
EOF
```

### nodeport 로 외부에서 접속

http://34.64.97.52/:30002

id : team2@samsung.com   
pw : team2     

gke의 node 외부 ip는 변경될 수 있음으로 접속 안될때 확인 필요   
kubectl get node -o wide

### query
```

##################
flow 조회
##################
select f.flow_nm, d.api_seq, a.api_nm, d.is_last, d.api_timeout, d.api_retry, d.skip_error
from flowmanagerapi_flow f
,flowmanagerapi_api a
,flowmanagerapi_flow_dtl d
where f.flow_id = d.flow_id
and   a.api_id = d.api_id
and f.flow_nm ='flow_6_1'
;


#############
job 추적
#############
select f.flow_nm, d.api_seq, a.api_nm, d.is_last, d.api_timeout, d.api_retry, d.skip_error
,j.run_job_id, j.api_status, j.api_start_dt, j.api_end_dt
from flowmanagerapi_flow f
,flowmanagerapi_api a
,flowmanagerapi_flow_dtl d
,flowmanagerapi_flow_job j
where f.flow_id = d.flow_id
and   a.api_id = d.api_id
and   d.flow_dtl_id=j.flow_dtl_id
and   j.run_job_id='test_runtime_0802_2'
order by j.api_start_dt
;



#############
job timeout checker 추적
#############
select f.flow_nm, d.api_seq, a.api_nm, d.is_last
,j.run_job_id, j.api_status, j.api_start_dt, j.api_end_dt
,cj.check_status
,cj.check_start_dt
,cj.check_end_dt
from flowmanagerapi_flow f
,flowmanagerapi_api a
,flowmanagerapi_flow_dtl d
,flowmanagerapi_flow_job j
,flowmanagerapi_check_job cj
where f.flow_id = d.flow_id
and   a.api_id = d.api_id
and   d.flow_dtl_id=j.flow_dtl_id
and   j.run_job_id=cj.checker_id
and   j.run_job_id='job0729-2'
;
```
