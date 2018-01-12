from django.conf.urls import url, include
from django.contrib import admin

from hms.views.admin import invite
from hms.views.doctor import costs

urlpatterns = [
    url(r'^admin/invite/$',invite, name="invite"),
    url(r'^admin/costs/$',costs,name="add_costs")
]
