from rest_framework import serializers
from flowmanagerapi.models import FLOW, FLOW_DTL, API, FLOW_JOB, CHECK_JOB
from django.contrib.auth.models import User

class FLOWSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FLOW
        fields = '__all__'
        
class FLOW_DTLSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FLOW_DTL
        fields = '__all__'
        
class APISerializer(serializers.ModelSerializer):
    
    class Meta:
        model = API
        fields = '__all__'
        
class FLOW_JOBSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FLOW_JOB
        fields = '__all__'

class CHECK_JOBSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CHECK_JOB
        fields = '__all__'        

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'  