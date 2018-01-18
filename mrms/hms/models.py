# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from mrms.models import DateTimeModel
from usermanagement.models import User
# Create your models here.


class HospitalTypes(DateTimeModel):
    hospital_types = (
        ("clinic", "Private Clinic"),
        ("24*7", "A full fledged Hospital"),
        ("cancerclinic", "Cancer Clinic")
    )
    hospital_type = models.CharField(max_length=120, choices=hospital_types)

    def __str__(self):
        return self.hospital_type


class Department(DateTimeModel):
    dept_id = models.CharField(max_length=100, blank=False, null=False)
    dept_name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        unique=True)
    dept_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.dept_name


class Hospital(DateTimeModel):
    hospital_name = models.CharField(
        max_length=500,
        blank=False,
        null=False,
        verbose_name="Name of the Hospital")
    hospital_location = models.TextField(
        verbose_name="Full Address of the Hospital")
    hospital_type = models.ForeignKey(
        HospitalTypes,
        blank=False,
        null=False,
        verbose_name="Type of Hospital",
        on_delete=models.PROTECT)
    hospital_descrition = models.TextField(blank=True, null=True)
    hospital_reg_no = models.CharField(
        max_length=300,
        blank=False,
        null=False,
        default="",
        verbose_name="Hospital Registration Number")
    hospital_registered_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.hospital_name


class DepartmentsInHospital(DateTimeModel):
    hospital_dept_id = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name="Internal Department ID")
    hospital_id = models.ForeignKey(
        Hospital,
        blank=False,
        null=False,
        verbose_name="Which Hopspital ?", on_delete=models.PROTECT)
    dept = models.ForeignKey(
        Department,
        verbose_name="Select Department",
        to_field="dept_name", on_delete=models.PROTECT)
    no_of_doctors = models.IntegerField(
        verbose_name="How many doctors are there in this Dept")
    dept_location = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Where is this Dept located in the hospital")
    dept_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Any other specific details")

    def __str__(self):
        return "%s - %s" % (self.hospital_id.hospital_name,
                            self.dept.dept_name)


class BillingComponents(DateTimeModel):
    component_types = (
        ('mandatory', 'Mandatory like Consultation Cost'),
        ('optional', 'Optional'),
        ('onetime', 'OneTime Cost')
    )
    hospital_ref_id = models.ForeignKey(
        Hospital, related_name="hospital_ref_id",default=1)
    created_by = models.ForeignKey(User, related_name="created_by",default=1)
    updated_by = models.ForeignKey(User, related_name='updated_by',default=1)
    billing_component = models.TextField(verbose_name="What is the cost about")
    component_cost = models.PositiveIntegerField(
        verbose_name="What is the cost")
    component_type = models.CharField(
        max_length=30,
        verbose_name="Mandatory or Optional or One Time Cost",
        choices=component_types)

    def __str__(self):
        return self.billing_component

class HospitalUserRole(DateTimeModel):
    role_choices = (
        ('receptionist','Receptionist'),
        ('doctor','Doctor'),
        ('hospital_admin','Hospital Admin'),
        ('accounts','Accounts'),
        ('accounts_admin','Accounts Admin')
    )
    hospital_reference = models.ForeignKey(Hospital, related_name="hospital_user_role_hospital_id")
    user_reference = models.ForeignKey(User, related_name="hospital_user_role_user_id")
    role = models.CharField(max_length=20, choices=role_choices)

    def __str__(self):
        return "%s - %s - %s"%(self.hospital_reference, self.user_reference, self.role)

class Invitations(DateTimeModel):

    invite_user_reference = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital_invited_into = models.ForeignKey(
        Hospital, related_name="hospital_invited_into")
    invited_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="invited_by")
    is_invitation_notified = models.BooleanField(default=False)
    is_user_logged_in = models.BooleanField(default=False)
