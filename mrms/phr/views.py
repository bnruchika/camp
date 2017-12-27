# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from usermanagement.models import User
from usermanagement.decorators import doctor_profile_validated

from phr.models import PatientAllergies, PatientEvents, PatientSymptoms

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
            return render(request, "find_patient.html", {'patient': patient})
        else:
            return render(
                request, "find_patient.html", {
                    'error': "Patient with this mobile number not found"})
    else:
        return render(request, "find_patient.html")


def event_details(request, username, event_id=None):
    return_dict = {}
    try:
        patient = User.objects.get(username=request.user.username)
        return_dict["patient"] = patient
    except ObjectDoesNotExist:
        raise Exception("Patient Not Found")
    # Get the list of patient Allergies. This will for sure lead to a confusion. Need to handle it
    # Which doctor is right is the confusion
    allergies, status = PatientAllergies.objects.get_or_create(user=patient)
    return_dict["allergies"] = allergies

    # BUG : What if someone keeps changing the event id just like that.
    # TODO : Figure out when to close an event
    if event_id:
        try:
            event = PatientEvents.objects.get(id=event_id)
            return_dict["event"] = event
        except ObjectDoesNotExist:
            error = "Unknown event ID for the patient. Do not edit the url from the screen."
            raise Exception(error)
    else:
        symptoms = PatientSymptoms.objects.create(
            doctor_reported_symptoms="", user=return_dict['patient'])
        symptoms.save()
        event = PatientEvents.objects.create(
            user=return_dict['patient'],
            hospital_id="1",
            dept_id="1",
            doctor_id="1",
            schedule_date=datetime.date.today(),
            symptoms=symptoms,
            is_open=True
        )
        return_dict["event"] = event
    history = PatientEvents.objects.filter(user=request.user)
    return_dict["history"] = history
    return render(
        request, "patient_details.html", return_dict)
