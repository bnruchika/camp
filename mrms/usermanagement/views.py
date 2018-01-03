# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


from usermanagement.forms import SignUpForm, LoginForm, DoctorProfileForm
from usermanagement.models import User

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'usermanagement/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            # Bad login details were provided. So we can't log the user in.
            form = LoginForm()
            error = "User not found"
            return render(request, 'usermanagement/login.html',
                          {'form': form, 'error': error})
    else:
        form = LoginForm()
        return render(request, 'usermanagement/login.html', {'form': form})


@login_required
def profile(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        form = DoctorProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.doctor_activated = True
            user.save()
            return HttpResponseRedirect("/")
        else:
            return render(request,
                          'usermanagement/doctor_profile.html',
                          {'form': form})
    else:
        try:
            doctor_profile = User.objects.get(username=request.user.username)
            form = DoctorProfileForm(instance=doctor_profile)
        except ObjectDoesNotExist:
            form = DoctorProfileForm(request=request)
        return render(request,
                      'usermanagement/doctor_profile.html',
                      {'form': form})


# TODO: Need to make forgot password and delete account working
