# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from mrms.models import DateTimeModel

from usermanagement.models import User

from hms.models import Hospital, DepartmentsInHospital


class PatientOperation(DateTimeModel):
    operation_name = models.TextField(blank=False, null=False)
    operation_details = models.TextField(blank=False, null=False)

    # Operation performed by ?
    tenant_id = models.CharField(max_length=50, default="Atom360", blank=False,
                                 null=False)
    hospital_id = models.CharField(max_length=50, blank=False, null=False)
    dept_id = models.CharField(max_length=50, blank=False, null=False)

    # This can take a list with the help of ast to decouple it
    doctor_id = models.CharField(max_length=50, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class PatientAdmission(DateTimeModel):
    admission_reference_id = models.CharField(max_length=100, blank=False,
                                              null=False)
    admission_date = models.DateTimeField(blank=False, null=False)
    discharge_date = models.DateTimeField(blank=True, null=True)
    discharge_note = models.TextField()
    operation = models.ForeignKey(
        PatientOperation,
        blank=True,
        null=True,
        on_delete=models.PROTECT)
    inpatient_observation = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class PatientInjection(DateTimeModel):
    injection_name = models.CharField(max_length=200, blank=True, null=True)
    injection_dose = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class PatientSymptoms(models.Model):
    patient_reported_symptoms = models.TextField(blank=True, null=True)
    doctor_reported_symptoms = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

class PatientDiseases(models.Model):
    #patient_reported_symptoms = models.TextField(blank=True, null=True)
    patient_diseases = models.TextField(blank=False, null=False, default ="")
    user = models.ForeignKey(User, on_delete=models.PROTECT)



class PatientMedicines(DateTimeModel):
    cycle_choices = (
        ("as_pain", "Whenever you have pain"),
        ("101(A)", "Morning & Night after Food"),
        ("101(B)", "Morning & Night before Food"),
        ("111(B)", "3 times a day before Food"),
        ("111(A)", "3 times a day after Food"),
        ("001(A)", "Only night after food"),
        ("001(B)", "Only night before food"),
    )
    medicine_name = models.CharField(max_length=200, blank=False, null=False)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    dosage = models.CharField(max_length=50, blank=False, null=False)
    cycle = models.CharField(max_length=50, choices=cycle_choices)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.medicine_name


class PatientTests(DateTimeModel):
    # test names should be loaded from a pre-defined set of templates
    test_name = models.CharField(max_length=100, blank=False, null=False)
    test_date = models.DateField()  # When to do the test
    test_condition = models.TextField(blank=True, null=True)
    test_results = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class PatientAllergies(DateTimeModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    allergy = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        default="")


class DCMImages(DateTimeModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    pic = models.ImageField()


class PatientEvents(DateTimeModel):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="patient_id")
    tenant_id = models.CharField(max_length=50, default="Atom360", blank=False,
                                 null=False)
    hospital_id = models.ForeignKey(Hospital, on_delete=models.PROTECT)
    dept_id = models.ForeignKey(
        DepartmentsInHospital,
        on_delete=models.PROTECT)
    doctor_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="doctor_id")
    visit_date = models.DateField(auto_now=True)
    schedule_date = models.DateField(blank=False, null=False)
    symptoms = models.ForeignKey(PatientSymptoms, on_delete=models.PROTECT)
    diseases = models.ForeignKey(PatientDiseases, on_delete=models.PROTECT, default=1)
    medicines = models.ManyToManyField(PatientMedicines)
    injection = models.ManyToManyField(PatientInjection)
    dcmimages = models.ManyToManyField(DCMImages, blank=True, null=True)
    tests = models.ManyToManyField(PatientTests)
    clinical_advice = models.TextField(blank=True, null=True)
    doctor_notes = models.TextField(blank=True, null=True)
    admission_required = models.BooleanField(default=False)
    admission_id = models.ForeignKey(
        PatientAdmission,
        blank=True,
        null=True,
        on_delete=models.PROTECT)
    next_vist_date = models.DateField(blank=True, null=True)
    is_open = models.BooleanField(default=False)
