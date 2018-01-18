from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from hms.forms import BillingCreationUpdationForm, UserInvitationForm
from hms.models import BillingComponents, Hospital, Invitations
from usermanagement.models import User
from usermanagement.decorators import validate_user_role_permission


@login_required
@validate_user_role_permission('hospital_admin')
def invite(request):

    # TODO: Currently three is no way to figure out which user belongs to which hospital
    # So using the default hospital
    hospital = Hospital.objects.get(id=1)
    if request.method =="POST":
        userinvitationform = UserInvitationForm(request.POST)
        if userinvitationform.is_valid():
            # Get all the data and map it for variables
            mobile_number = request.POST.get('mobile_number')
            name = request.POST.get('full_name')
            gender = request.POST.get('gender')
            email = request.POST.get('email')
            role = request.POST.get('role')
            # Check if user exists else create username
            try:
                user = User.objects.get(username=mobile_number)
            except ObjectDoesNotExist:
                user = User.objects.create(username=mobile_number,gender=gender,email=email, fullname=name)
                user.set_password("password")
                if role == "doctor":
                    user.is_doctor = True
                user.save()
            # Now create an invitation to be sent out
            invitation = Invitations.objects.create(
                hospital_invited_into=hospital,
                invite_user_reference=user,
                invited_by=User.objects.get(username=request.user.username)
            )
            invitation.save()
            # TODO : Email to be sent here .
            send_mail(
                'Registration Successful',
                'As a Doctor',
                'me_the_3d@hotmail.com',
                [user.email],
                fail_silently=False,
            )
            invitation.is_invitation_notified = True
            invitation.save()

            # Assign the role for the user in the hospital
            hospitalrole = HospitalUserRole.objects.create(
                hospital_reference=hospital,
                user_reference=user,
                role=role
                )
            hospitalrole.save()
    userinvitationform = UserInvitationForm()
    invitations = Invitations.objects.filter(hospital_invited_into=hospital)
    return render(request,
                  'hms/user_invitation.html',
                  {
                      'userinvitationform':userinvitationform,
                      'invitations':invitations
                   }
                  )


@login_required
@validate_user_role_permission('accounts_admin')
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
        costs = BillingComponents.objects.filter(
            hospital_ref_id=hospital)
        return render(request,
                      'hms/admin_billing.html',
                      {'mandatory_costs': mandatory_costs,
                       optional_costs: 'optional_costs',
                       "onetime_costs": onetime_costs,
                       "costs": costs,
                       'billingform': billingform})
