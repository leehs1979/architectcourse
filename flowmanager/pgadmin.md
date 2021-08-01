
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
