from usermanagement.models import User
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist


def doctor_profile_validated(function):

    def check_doctor_valid_data(request, *args, **kwargs):
        try:
            doctor = User.objects.get(username=request.user.username)
            if doctor.is_doctor and doctor.doctor_activated:
                return function(request, *args, **kwargs)
            elif doctor.is_doctor:
                return HttpResponseRedirect("/user/profile/")
            else:
                return HttpResponseRedirect("/")
        except ObjectDoesNotExist:
            return HttpResponseRedirect("/user/profile/")

    return check_doctor_valid_data
