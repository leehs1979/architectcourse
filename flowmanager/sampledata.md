### Flow Sample Data

- API   
api_desc : api 시퀀스를 의미로 사용

![image](https://user-images.githubusercontent.com/10610884/124053037-746acc00-da5a-11eb-84c5-0b5ba80b53ca.png)


- Flow   

Flow_nm 규칙 : flow_{api개수}_{flow시퀀스}   
flow_desc : api 개수 의미   

![image](https://user-images.githubusercontent.com/10610884/124053099-96644e80-da5a-11eb-9427-cd519e1db6ee.png)


- Flow - API 매핑

규칙 :    
 api 개수만큼 sync - async를 반복적으로 구성 (api 개수는 짝수로 구성)   
 timeout : sync->10초 / async->20초   

![image](https://user-images.githubusercontent.com/10610884/124053607-86993a00-da5b-11eb-84fc-c991697f810c.png)


### 쿼리

- Flow - API 맵핑 
```
insert into flowmanagerapi_flow_dtl
select gen_random_uuid() as flow_dtl_id
      ,ROW_NUMBER() OVER( PARTITION BY flow_nm) AS api_seq
	  --, api_nm
      ,api_timeout
      ,3 as api_retry
      ,'Leehs' as creator
	  ,now() as created
	  ,api_id
	  ,flow_id
	  --,'N' as is_last
	  ,case when ROW_NUMBER() OVER( PARTITION BY flow_nm) = flow_desc::INTEGER then 'Y' else 'N' end as is_last -- flow api개수 
from (
	select a.flow_id
		 , a.flow_nm
		 , b.api_id
		 , b.api_nm
		 , case when b.api_type='sync' then 10 else 20 end as api_timeout --timeout 
		 , a.flow_desc
	from flowmanagerapi_flow a
		,flowmanagerapi_api b
	where b.api_desc::INTEGER <= a.flow_desc::INTEGER/2    -- api개수 / 2 
	order by a.flow_nm,b.api_desc::INTEGER, b.api_nm desc
) x ;

```

- 매핑 검증
```
select f.flow_nm, d.api_seq, a.api_nm, d.is_last, d.api_timeout, d.api_retry
from flowmanagerapi_flow f
,flowmanagerapi_api a
,flowmanagerapi_flow_dtl d
where f.flow_id = d.flow_id
and   a.api_id = d.api_id
and f.flow_nm ='flow_10_1';
```

- 초기화 

```
## schema 출력
pg_dump -U team2 -t 'public.flowmanagerapi_flow_dtl' -t ' --schema-only mydb

## 테이블 초기화 
truncate table flowmanagerapi_flow_dtl  cascade ;
truncate table flowmanagerapi_check_job cascade;
truncate table flowmanagerapi_flow_job  cascade;
truncate table flowmanagerapi_flow      cascade;
truncate table flowmanagerapi_api       cascade;


## 컬럼 추가 
ALTER TABLE flowmanagerapi_flow_dtl ADD COLUMN is_last varchar(5);
 
```

- Drop Table
```
drop table auth_group                 cascade;
drop table auth_group_permissions     cascade;
drop table auth_permission            cascade;
drop table auth_user                  cascade;
drop table auth_user_groups           cascade;
drop table auth_user_user_permissions cascade;
drop table django_admin_log           cascade;
drop table django_content_type        cascade;
drop table django_migrations          cascade;
drop table django_session             cascade;
drop table flowmanagerapi_api         cascade;
drop table flowmanagerapi_check_job   cascade;
drop table flowmanagerapi_flow        cascade;
drop table flowmanagerapi_flow_dtl    cascade;
drop table flowmanagerapi_flow_job    cascade;
```


- Insert flow
[insert_flow.txt](https://github.com/leehs1979/architectcourse/files/6889559/insert_flow.txt)
- Insert api
[insert_api.txt](https://github.com/leehs1979/architectcourse/files/6889562/insert_api.txt)

