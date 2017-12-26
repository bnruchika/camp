# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from usermanagement.models import User
from usermanagement.decorators import doctor_profile_validated

from phr.models import PatientAllergies, PatientEvents

# Create your views here.


@login_required
@doctor_profile_validated
def find_patient(request):
    if request.method == "POST":
        # make a post to ehr here.
        username = request.POST.get("mobile_number")
        patient = User.objects.get(username=username)
        # TODO : Handle other cases
        if patient:
            return render(request, "find_patient.html",{'patient':patient})
        else:
            return render(request, "find_patient.html",{'error':"Patient with this mobile number not found"})
    else:
        return render(request, "find_patient.html")


def event_details(request, username, event_id=None):
    return_dict = {}
    try:
        patient = User.objects.get(username=request.user.username)
        return_dict["patient"] = patient
    except ObjectDoesNotExist:
        raise Exception("Patient Not Found")

    # BUG : What if someone keeps changing the event id just like that.
    if event_id:
        event = PatientEvent.objects.get_or_create(id=event_id)
        return_dict["event"] = event
    # Get the list of patient Allergies. This will for sure lead to a confusion. Need to handle it
    # Which doctor is right is the confusion
    allergies, status = PatientAllergies.objects.get_or_create(user=request.user)
    return_dict["allergies"] = allergies
    return render(
        request, "patient_details.html", return_dict)
