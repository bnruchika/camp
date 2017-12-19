# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#Django specific imports
from django.db import models
from django.contrib.auth.models import AbstractUser

#App specific imports
from mrms.models import DateTimeModel


class StateMedicalCouncil(DateTimeModel):
    state_medical_council_id = models.IntegerField(
        blank=False, null=False, primary_key=True,verbose_name="Enter medical code as per : https://www.mciindia.org/ActivitiWebClient/informationdesk/indianMedicalRegister")
    state_medical_council_name = models.CharField(
        max_length=150, blank=False, null=False)

    def __str__(self):
        return self.state_medical_council_name

class User(AbstractUser):
    gender_choices = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    )
    gender = models.CharField(max_length=10, choices=gender_choices,default="undisclosed")
    # TODO : The baddest implementation that can ever be done. Do fix it without fail
    dob = models.DateField(default="1987-09-13")
    is_doctor = models.BooleanField(default=False)
    doctor_activated = models.BooleanField(default=False)
    doctor_registration_number = models.CharField(
        max_length=50,
        blank=False,
        null=True,
        default=None,
        verbose_name="Medical Council Registration Number")
    doctor_state_medical_council = models.ForeignKey(
        StateMedicalCouncil, blank=False, null=True,default=None, on_delete=models.PROTECT, verbose_name="Medical Council")
    doctor_date_of_reg = models.DateField(
        blank=False, null=True,default=None, verbose_name="Date of Registration")
