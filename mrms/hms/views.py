from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


def invite(request):
    pass

# TODO: Need to
@login_required
def costs(request):
    pass
