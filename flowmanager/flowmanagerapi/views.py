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
    
    def job(self, args):
        print("I'm working..."+args, "| [time] "
          , str(time.localtime().tm_hour) + ":"
          + str(time.localtime().tm_min) + ":"
          + str(time.localtime().tm_sec))

    def job_2(self):
        print("Job2 실행: ", "| [time] "
          , str(time.localtime().tm_hour) + ":"
          + str(time.localtime().tm_min) + ":"
          + str(time.localtime().tm_sec))
        
    def checkAsyncTimeout(self, id):
        print("check async timeout : [ID] "+id)
        print(datetime.now())
        
        # TODO: Timeout 
    
    def create(self, request, *args, **kwargs):   # TODO: Apscheduler Set
        
        print("Test create override called")
                
        self.serializer_class = self.serializer_class
        
        # TODO: Hooking Point
        
        return super().create(request, *args, **kwargs)
        '''
        
        try:    
            
            # test
            print("schedule called")
            testFlag = True
            if testFlag:
                raise Exception('Test')
            
            # APScheduler call 하고 나머지는 그대로 입력한다.
            
            # date : 1번만 실행
            # 현재 시간 + 30초(Timeout)
            flow_id = str(datetime.now())
            print(datetime.now())
            
            # Timeout Check Scheduler 등록
            sched.add_job(self.checkAsyncTimeout, 'date', run_date=(datetime.now()+timedelta(seconds=10)), id=flow_id, args=[flow_id])
            
            # 정상 처리면 Timeout Check Scheduler 해제
            #if True:
            #    sched.remove_job(flow_id)
            
            # interval - 매 3조마다 실행
            #sched.add_job(self.job, 'interval', seconds=3, id="test_2",  args=['pass_args'])
           
            # 즉시 실행
            #sched.add_job(my_job, args=['text'])
            
            # username = request.data['username']       
            # user = User.objects.get(username=username)

            # user.is_active = False
            # user.save() 
           
            response = {'message': 'schedule is done successfully', 'result': 'result__'}
            return Response(response, status = status.HTTP_200_OK)
            
        except Exception as ex:
            logger.error('Error Occured while processing schedule : %s' % ex)
                    
            response = {'message': 'schedule failed.'}            
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR) 
        '''
    
    # https://tech.serhatteker.com/post/2020-09/enable-partial-update-drf/
    # 호출시 ID를 주어야 한다. DELETE도 마찬가지
    def update(self, request, *args, **kwargs): 
        
        print("update called")
        
        kwargs['partial'] = True
        
        # TODO: Apscheduler Status Set
        
        return super().update(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]


