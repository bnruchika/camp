# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#Django specific imports
from django.db import models
from django.contrib.auth.models import AbstractUser

#App specific imports
from mrms.models import DateTimeModel


from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, username, dob, gender, fullname, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an phone number')

        user = self.model(
            email=username,
            dob = dob,
            gender=gender,
            fullname=fullname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, dob, gender, fullname, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(username),
            dob = dob,
            gender=gender,
            fullname=fullname
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



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

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

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
