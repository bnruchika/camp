from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse


from hms.forms import BillingCreationUpdationForm
from hms.models import BillingComponents, Hospital

# TODO: Need to


@login_required
def invite(request):
    pass


@login_required
def costs(request):
    hospital = Hospital.objects.get(id=1)
    if request.method == "POST":
        if request.POST.get("action") == "delete":
            cost_id = request.POST.get('cost_id')
            component = BillingComponents.objects.get(id=cost_id)
            component.delete()
        else:
            billingform = BillingCreationUpdationForm(
                request.POST, request=request)
            if billingform.is_valid():
                billingform.save()
        return HttpResponseRedirect(reverse('add_costs'))
    elif request.method == "GET":
        billingform = BillingCreationUpdationForm()
        mandatory_costs = BillingComponents.objects.filter(
            hospital_ref_id=hospital, component_type="mandatory")
        optional_costs = BillingComponents.objects.filter(
            hospital_ref_id=hospital, component_type="optional")
        onetime_costs = BillingComponents.objects.filter(
            hospital_ref_id=hospital, component_type="onetime")
        return render(request,
                      'hms/admin_billing.html',
                      {'mandatory_costs': mandatory_costs,
                       optional_costs: 'optional_costs',
                       "onetime_costs": onetime_costs,
                       'billingform': billingform})
