from django.conf.urls import url, include
from django.contrib import admin

from mrms.views import home

from phr.views import find_patient, event_details, update_patient_symptoms

urlpatterns = [
               url(r'^find$',
                   find_patient,
                   name="find_patient"),
               url(r'^details/(?P<username>\d+)/$',
                   event_details,
                   name="event_details"),
               url(r'^details/(?P<username>\d+)/(?P<event_id>\d+)/$',
                   event_details,
                   name="event_details"),
               url(r'^update_symptoms/$',
                   update_patient_symptoms,
                   name="update_patient_symptoms"),

               ]
