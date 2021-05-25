from django.db import models
import uuid
from datetime import datetime

# Create your models here.
class FLOW(models.Model):
    # PK
    flow_id = models.UUIDField(verbose_name="flowpid",primary_key=True, default=uuid.uuid4, editable=False)
    flow_nm = models.CharField(max_length=100, null=False, blank=False)
    flow_desc = models.TextField(max_length=500, null=True, blank=True)
    
    creator = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="date create")
    
    def __str__(self):
        return self.flow_nm

    class Meta:
        ordering = ['created']
        
class API(models.Model):
    # PK
    api_id = models.UUIDField(verbose_name="apiid",primary_key=True, default=uuid.uuid4, editable=False)
    api_nm = models.CharField(max_length=100, null=False, blank=False)
    api_desc = models.TextField(max_length=500, null=True, blank=True)
    api_type = models.TextField(max_length=100, null=True, blank=True)          # sync / async
    api_result_type = models.TextField(max_length=100, null=True, blank=True)   # Callback / ResultAPI
    api_uri = models.TextField(max_length=100, null=True, blank=True)
    api_provider = models.TextField(max_length=100, null=True, blank=True)
    
    api_in_format = models.TextField(max_length=100, null=True, blank=True)     # json : in-format
    api_out_format = models.TextField(max_length=100, null=True, blank=True)    # json : out-format
    
    creator = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="date create")
    
    def __str__(self):
        return self.api_nm

    class Meta:
        ordering = ['created']
        
class FLOW_DTL(models.Model):
    # PK
    flow_dtl_id = models.UUIDField(verbose_name="flowdtlid",primary_key=True, default=uuid.uuid4, editable=False)
    
    # FK
    flow = models.ForeignKey(FLOW, on_delete=models.CASCADE) # flow_id
    api = models.ForeignKey(API, on_delete=models.CASCADE)   # api_id
    api_seq = models.PositiveIntegerField(default=0)
    
    api_timeout = models.PositiveIntegerField(default=10)   # second
    api_retry = models.PositiveIntegerField(default=3)      # count
    
    creator = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="date create")
    
    def __str__(self):
        return self.flow_nm

    class Meta:
        unique_together = ('flow', 'api', 'api_seq')
        ordering = ['created']
        
class FLOW_JOB(models.Model):
    # PK
    flow_job_id = models.UUIDField(verbose_name="jobid",primary_key=True, default=uuid.uuid4, editable=False)
    
    # FK
    flow_dtl = models.ForeignKey(FLOW_DTL, on_delete=models.CASCADE)         # flow_dtl_id, ERD 상의 seq(FK) 대신 사용
        
    api_input = models.TextField(max_length=1000, null=True, blank=True)     # json : input
    api_output = models.TextField(max_length=1000, null=True, blank=True)    # json : output
    api_status = models.CharField(max_length=50, null=True, blank=True)
    
    api_start_dt = models.DateTimeField(auto_now=True, verbose_name="start time")
    api_end_dt = models.DateTimeField(auto_now=True, verbose_name="end time")    
        
    creator = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="date create")

    class Meta:
        ordering = ['created']                        