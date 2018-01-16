from hms.models import Hospital, HospitalUserRole
from usermanagement.models import User


def get_user_role_entity(request):
    hospital = Hospital.objects.get(id=1)
    #import pdb;pdb.set_trace()
    role = HospitalUserRole.objects.filter(hospital_reference=hospital, user_reference=User.objects.get(username=request.user.username))
    if len(role) > 0:
        return role[0].role
    else:
        return False

def is_hospital_doctor(request):
    hospital = Hospital.objects.get(id=1)
    #import pdb;pdb.set_trace()
    role = HospitalUserRole.objects.filter(hospital_reference=hospital, user_reference=User.objects.get(username=request.user.username))
    if len(role) > 0 and role[0].role == "doctor":
        return True
    else:
        return False


def is_hospital_admin(request):
    hospital = Hospital.objects.get(id=1)
    #import pdb;pdb.set_trace()
    role = HospitalUserRole.objects.filter(hospital_reference=hospital, user_reference=User.objects.get(username=request.user.username))
    if len(role) > 0 and role[0].role == "hospital_admin":
        return True
    else:
        return False
