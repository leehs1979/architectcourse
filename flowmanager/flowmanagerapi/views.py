from django.shortcuts import render

from flowmanagerapi.models import FLOW, FLOW_DTL, API, FLOW_JOB, CHECK_JOB
from django.contrib.auth.models import User
from flowmanagerapi.serializers import FLOWSerializer, FLOW_DTLSerializer, APISerializer, FLOW_JOBSerializer, CHECK_JOBSerializer, UserSerializer

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer

from datetime import date, datetime, timedelta
import time
import traceback

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError

import logging
logger = logging.getLogger(__name__)

sched = BackgroundScheduler()
sched.start()   

# Create your views here.
class FLOWViewSet(viewsets.ModelViewSet):
    queryset = FLOW.objects.all()
    serializer_class = FLOWSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['flow_nm', 'creator']
    search_fields = ['flow_nm']

class FLOW_DTLViewSet(viewsets.ModelViewSet):
    queryset = FLOW_DTL.objects.all()
    serializer_class = FLOW_DTLSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['flow', 'creator']
    search_fields = ['flow']

class APIViewSet(viewsets.ModelViewSet):
    queryset = API.objects.all()
    serializer_class = APISerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['api_nm', 'creator']
    search_fields = ['api_nm']

class FLOW_JOBViewSet(viewsets.ModelViewSet):
    queryset = FLOW_JOB.objects.all()
    serializer_class = FLOW_JOBSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['api_status', 'creator']
    
class CHECK_JOBViewSet(viewsets.ModelViewSet):
    queryset = CHECK_JOB.objects.all()
    serializer_class = CHECK_JOBSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['check_status', 'creator']
    
    def checkTimeout(self, checker_id, flow_job):
        
        print("check timeout : [chekcer_id] ", checker_id)
        print("check timeout : [flow_job] ", flow_job)
        print("time :",datetime.now())
        
        # Timeout 처리, check_job 테이블에 STATUS = TIMEOUT으로 설정
        try:
            check_job = CHECK_JOB.objects.get(checker_id=checker_id, flow_job=flow_job)
            check_job.check_status = 'TIMEOUT'
            check_job.save()
            
        except Exception as ex:
            print('Error Occured while processing checkTimeout : %s' % ex)
            print('[TRACE]', traceback.format_exc())
        
    
    def create(self, request, *args, **kwargs):   # Apscheduler Set
        
        print('[START] Scheduler Create')
                
        self.serializer_class = self.serializer_class
        
        ''' 넘어오는 값
        payload = {                
            "check_status": "STARTED",
            "check_start_dt": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f'),
            "checker_id": service['run_job_id'],
            "creator": "Team2",
            "flow_job": flow_job_id,
            "timeout": service['api_timeout']
        }
        '''

        # Step1: Flow_id 및 데이터 확인(json)
        # 예: a138634c-29d1-43cb-9e41-99dbc911e777
        req_data = request.data
                
        #check_status = req_data['check_status']
        #check_start_dt = req_data['check_start_dt']        
        #creator = req_data['creator']
        checker_id = req_data['checker_id']
        flow_job = req_data['flow_job']
        timeout = req_data['timeout']
        
        print("create : [chekcer_id] ", checker_id)
        print("create : [flow_job] ", flow_job)
        print("create : [timeout] ", timeout)
        print("time :",datetime.now())             
        
        # Step2: Timeout Check Scheduler 등록 -> id = checker_id+flow_job => delete 시에 사용한다.
        try:
             
            sched.add_job(self.checkTimeout, 'date', run_date=(datetime.now()+timedelta(seconds=timeout)), id=checker_id+flow_job, args=[checker_id, flow_job])
                        
        except Exception as ex:
            print('Error Occured while processing schedule create : %s' % ex)
            print('[TRACE]', traceback.format_exc())
        
        print('[END] Scheduler Create')
        # check_job 테이블에 INSERT
        return super().create(request, *args, **kwargs)
    
    # https://tech.serhatteker.com/post/2020-09/enable-partial-update-drf/
    # 호출시 ID를 주어야 한다. DELETE도 마찬가지
    def update(self, request, *args, **kwargs): 
        
        print('[START] Scheduler Update')
        
        kwargs['partial'] = True
        
        '''
        payload = {                
            "check_status": "CANCEL",
            "check_end_dt": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f'),
            "checker_id": service['run_job_id'],
            "flow_job": flow_job_id
        }
        '''     
        
        req_data = request.data
        
        #check_status = req_data['check_status']
        #check_end_dt = req_data['check_end_dt']
        checker_id = req_data['checker_id']
        flow_job = req_data['flow_job']
        
        print("update : [chekcer_id] ", checker_id)
        print("update : [flow_job] ", flow_job)
        print("time :",datetime.now())
        
        # Timeout Job Remove
        try:
            sched.remove_job(checker_id+flow_job)                       
        
        except Exception as ex:
            print('Error Occured while processing schedule update : %s' % ex)
            print('[TRACE]', traceback.format_exc())
                
        print('[END] Scheduler Update')
        # check_job 테이블에 update
        return super().update(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]

