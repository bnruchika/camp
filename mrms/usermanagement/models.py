# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django specific imports
from django.db import models
from django.contrib.auth.models import AbstractUser

# App specific imports
from mrms.models import DateTimeModel


from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, username, dob, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an phone number')

        user = self.model(
            email=username,
            dob=dob,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, dob, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an phone number')

        user = self.model(
            username=username,
            dob=dob,
        )

        user.set_password(password)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class StateMedicalCouncil(models.Model):
    state_medical_council_id = models.IntegerField(
        blank=False,
        null=False,
        primary_key=True,
        verbose_name="Enter medical code as per : https://www.mciindia.org/ActivitiWebClient/informationdesk/indianMedicalRegister")
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
    blood_group_choices = (
        ('A+ve','A+ve'),
        ('B+ve','B+ve'),
        ('A-ve','A-ve'),
        ('B-ve','B-ve'),
        ('O+ve','O+ve'),
        ('O-ve','O-ve'),
        ('AB+ve','AB+ve'),
        ('AB-ve','AB-ve'),
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    fullname = models.CharField(max_length=400, default="Unknown")
    gender = models.CharField(
        max_length=10,
        choices=gender_choices,
        default="undisclosed")
    # TODO : The baddest implementation that can ever be done. Do fix it
    # without fail
    dob = models.DateField(default="1987-09-13")
    blood_group = models.CharField(max_length=5,choices=blood_group_choices,default="")
    is_doctor = models.BooleanField(default=False)
    doctor_activated = models.BooleanField(default=False)
    doctor_registration_number = models.CharField(
        max_length=50,
        blank=False,
        null=True,
        default=None,
        verbose_name="Medical Council Registration Number")
    doctor_state_medical_council = models.ForeignKey(
        StateMedicalCouncil,
        blank=False,
        null=True,
        default=None,
        on_delete=models.PROTECT,
        verbose_name="Medical Council")
    doctor_date_of_reg = models.DateField(
        blank=False,
        null=True,
        default=None,
        verbose_name="Date of Registration")
    experience = models.IntegerField(
        verbose_name="Years of Experience", default=0)
    doctor_available_time = models.CharField(
        max_length=50,
        default="",
        verbose_name="Available Times (9-1, 4-7)")
    doctor_bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="About Yourself")
    doctor_specialization = models.CharField(
        blank=True,
        null=True,
        verbose_name="Fields of Specialization",
        max_length=200)

    REQUIRED_FIELDS = ["dob"]

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
