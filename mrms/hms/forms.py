from django import forms
from hms.models import BillingComponents, Hospital
from usermanagement.models import User


class BillingCreationUpdationForm(forms.ModelForm):

    class Meta:
        model = BillingComponents
        exclude = [
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BillingCreationUpdationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        cd["hospital_ref_id"] = Hospital.objects.get(id=1)
        cd["created_by"] = User.objects.get(
            username=self.request.user.username)
        cd["updated_by"] = User.objects.get(
            username=self.request.user.username)
        return cd
