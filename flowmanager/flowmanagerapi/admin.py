from django.contrib import admin

# Register your models here.
from .models import FLOW, FLOW_DTL, API, FLOW_JOB
admin.site.register({FLOW, FLOW_DTL, API, FLOW_JOB})