from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from usermanagement.decorators import doctor_profile_validated


@login_required
@doctor_profile_validated
def home(request):
    if request.method == "POST":
        # make a post to ehr here.
        username = request.POST.get("mobile_number")
        patient, patient_status = make_post(
            "find_patient", {"username": username})
        # TODO : Handle other cases
        if patient:
            response_data = json.loads(
                unicodedata.normalize(
                    'NFKD', patient).encode(
                    'ascii', 'ignore'))
            # FIXME: For all inhumane reasons in the world, the JsonResponse took me more than 2 hours
            # without sending the correct response. I give up. anybody is free to fix this.
            # Dont bring simplejson as a solution. Just resort to json
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json")
        else:
            return JsonResponse(
                {"error": "No user found with this username", "username": username}, 201)
    else:
        return render(request, "find_patient.html")
