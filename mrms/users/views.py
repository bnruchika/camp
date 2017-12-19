# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from users.forms import SignUpForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            fullname = form.cleaned_data.get("full_name")
            user = authenticate(username=username, password=raw_password)
            gender = request.POST.get("gender")
            dob = request.POST.get('dob')
            userprofile = UserProfile.objects.create(
                gender=gender, dob=dob, user=user, fullname=fullname)
            userprofile.save()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})
