# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods

from usermanagement.models import User
from usermanagement.decorators import doctor_profile_validated

from phr.models import PatientAllergies, PatientEvents, PatientSymptoms, PatientMedicines, DCMImages, PatientDiseases, PatientTests
from hms.models import Hospital, DepartmentsInHospital, Department
# Create your views here.


def handle_uploaded_file(f, name):
    with open('media/' + name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
@doctor_profile_validated
def find_patient(request):
    if request.method == "POST":
        # make a post to ehr here.
        username = request.POST.get("mobile_number")
        try:
            patient = User.objects.get(username=username)
            return render(request, "find_patient.html", {'patient': patient})
        except ObjectDoesNotExist:
            return render(
                request, "find_patient.html", {
                    'error': "Patient with this mobile number not found"})
    else:
        return render(request, "find_patient.html")


@login_required
@doctor_profile_validated
def event_details(request, username, event_id=None):
    return_dict = {}
    try:
        patient = User.objects.get(username=username)
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
        try:
            event = PatientEvents.objects.filter(user=patient)
            if (len(event) > 0) and (event.order_by('-id')[0].is_open):
                return_dict["event"] = event.order_by('-id')[0]
            else:
                raise Exception(
                    "No open event found for patient. Need to create a new one")
        except Exception:
            symptoms = PatientSymptoms.objects.create(
                doctor_reported_symptoms="", user=return_dict['patient'])
            symptoms.save()
            diseases = PatientDiseases.objects.create(patient_diseases="",user = return_dict["patient"])
            diseases.save()

            event = PatientEvents.objects.create(
                user=return_dict['patient'],
                hospital_id=Hospital.objects.get(id=1),
                dept_id=DepartmentsInHospital.objects.get(id=1),
                doctor_id=User.objects.get(username=request.user.username),
                schedule_date=datetime.date.today(),
                symptoms=symptoms,
                diseases=diseases,
                is_open=True
            )
            event.save()

            return_dict["event"] = event
    history = PatientEvents.objects.filter(user=return_dict['patient'])
    return_dict["history"] = history
    return render(
        request, "patient_details.html", return_dict)


@require_http_methods(["POST"])
@login_required
@doctor_profile_validated
def update_patient_symptoms(request):
    event_id = request.POST.get("event_id")
    if event_id:
        event = PatientEvents.objects.get(id=event_id)
        symptoms = PatientSymptoms.objects.get(id=event.symptoms.id)
        symptoms.doctor_reported_symptoms = symptoms.doctor_reported_symptoms + \
            "," + request.POST.get("doctor_reported_symptoms")
        symptoms.save()
        return JsonResponse(
            {"symptoms": event.symptoms.doctor_reported_symptoms}, status=201)
    else:
        return JsonResponse(
            {"error": "Event Not Created. Register Patient First ?"}, status=500)
@require_http_methods(["POST"])
@login_required
@doctor_profile_validated
def update_patient_tests(request):
    event_id = request.POST.get("event_id")
    if event_id:
        event = PatientEvents.objects.get(id=event_id)
        user = event.user
        tests = PatientTests.objects.create(
            doctor_reported_tests=request.POST.get("doctor_reported_tests"),
            user=user,
            test_date = datetime.datetime.today()
            )
        tests.save()
        event.tests.add(tests)
        event.save()
        return JsonResponse(
            {"test_name": tests.doctor_reported_tests,"test_date":tests.test_date}, status=201)
    else:
        return JsonResponse(
            {"error": "Event Not Created. Register Patient First ?"}, status=500)


@require_http_methods(["POST"])
@login_required
#@doctor_profile_validated
def update_patient_diseases(request):
    event_id = request.POST.get("event_id")
    if event_id:
        event = PatientEvents.objects.get(id=event_id)
        diseases = PatientDiseases.objects.get(id=event.diseases.id)
        diseases.patient_diseases = diseases.patient_diseases + \
            "," + request.POST.get("patient_diseases")
        diseases.save()
        return JsonResponse(
            {"diseases": event.diseases.patient_diseases}, status=201)
    else:
        return JsonResponse(
            {"error": "Event Not Created. Register Patient First ?"}, status=500)

@require_http_methods(["POST"])
@login_required
@doctor_profile_validated
def update_patient_medicines(request):
    event_id = request.POST.get("event_id")
    if event_id:
        event = PatientEvents.objects.get(id=event_id)
        medicine_name = request.POST.get("med_name")
        dosage = request.POST.get("med_dosage")
        days = request.POST.get("days")
        cycle = request.POST.get("med_cycle")
        end_date = datetime.datetime.now() + datetime.timedelta(days=int(days))
        medicine = PatientMedicines.objects.create(
            medicine_name=medicine_name,
            dosage=dosage,
            end_date=end_date,
            cycle=cycle,
            user=event.user)
        medicine.save()

        event.medicines.add(medicine)
        response_dict = {
            "event_id": event.id,
        }
        return JsonResponse(
            {"success": "Added medicine successfully"}, status=201)
    else:
        return JsonResponse(
            {"error": "Event Not Created. Register Patient First ?"}, status=500)


@login_required
def upload_dcm_image(request):
    myfiles = request.FILES.getlist("dcmimages")
    patient_id = request.POST.get("patient_id")
    event_id = request.POST.get("event_id")
    for image in myfiles:
        # handle_uploaded_file(f,name)
        dcmimage = DCMImages(
            user=User.objects.get(
                username=request.user.username),
            pic=image)
        dcmimage.save()
        handle_uploaded_file(image, str(dcmimage.id))
        event = PatientEvents.objects.get(id=event_id)
        event.dcmimages.add(dcmimage)
        event.save()
    return HttpResponseRedirect(
        "/patient/details/%s/%s/" %
        (patient_id, event_id))


@login_required
def close_event(request):
    event_id = request.POST.get("event_id")
    event = PatientEvents.objects.get(id=event_id)
    event.is_open = False
    event.save()
    return HttpResponseRedirect("/patient/find/")
