from django.conf.urls import url, include
from django.contrib import admin

from hms.views import invite

urlpatterns = [
    url(r'^admin/$',invite, name="invite")
]
