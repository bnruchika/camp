"""mrms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from mrms.views import home

from phr.views import find_patient, event_details

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'auth/', include('usermanagement.urls')),
    url(r'user/', include('usermanagement.urls')),
    url(r'^$', home, name='home'),
    url(r'^find_patient/$', find_patient, name="find_patient"),
    url(r'^patient_details/(?P<username>\d+)/$', event_details, name="event_details"),
    url(r'^patient_details/(?P<username>\d+)/(?P<event_id>\d+)/$', event_details, name="event_details"),


]
