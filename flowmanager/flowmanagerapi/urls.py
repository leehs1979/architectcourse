from django.contrib import admin
from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns

from django.conf import settings
from django.conf.urls.static import static

# Using Router
from flowmanagerapi import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()  #  automatically creates the API root view
router.register(r'flow', views.FLOWViewSet)
# router.register(r'flow/schedule', views.FLOWViewSet)

router.register(r'flow_dtl', views.FLOW_DTLViewSet)
router.register(r'api', views.APIViewSet)
router.register(r'flow_job', views.FLOW_JOBViewSet)

router.register(r'check_job', views.CHECK_JOBViewSet)   # TODO: Check CRUD Override

# For user
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    #path('/rest-auth/', include('rest_auth.urls')),
    #path('/rest-auth/registration/', include('rest_auth.registration.urls'))
] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
