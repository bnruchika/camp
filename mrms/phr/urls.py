from django.conf.urls import url, include
from django.contrib import admin

from mrms.views import home

from phr.views import find_patient, event_details, update_patient_symptoms, update_patient_medicines, upload_dcm_image, close_event, update_patient_diseases,  update_patient_tests
urlpatterns = [
    url(r'^find/$',
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
    url(r'^update_diseases/$',
        update_patient_diseases,
        name="update_patient_diseases"),
    url(r'^update_tests/$',
        update_patient_tests,
        name="update_patient_tests"),

    url(r'^update_medicines/$',
        update_patient_medicines,
        name="update_patient_medicines"),
    url(r'^upload_dcm_image/$',
        upload_dcm_image,
        name="upload_dcm_image"),
    url(r'^close_event/$',
        close_event,
        name="close_event"),

]
