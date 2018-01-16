from usermanagement.models import User
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist


def doctor_profile_validated(function):

    def check_doctor_valid_data(request, *args, **kwargs):
        """ A decorator that will valiate if the logged in user is a doctor or not. If doctor and profile not updated, will force an update, else let use the system

        """
        try:
            doctor = User.objects.get(username=request.user.username)
            if doctor.is_doctor and doctor.doctor_activated:
                return function(request, *args, **kwargs)
            elif doctor.is_doctor:
                return HttpResponseRedirect("/user/profile/")
            else:
                # Not a doctor, so dont matter.
                return function(request, *args, **kwargs)
        except ObjectDoesNotExist as e:
            return HttpResponseRedirect("/auth/register/")

    return check_doctor_valid_data
