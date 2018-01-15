from django import forms
from hms.models import BillingComponents, Hospital, Invitations
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

class UserInvitationForm(forms.Form):

        gender_choices = (
            ('male', 'Male'),
            ('female', 'Female'),
            ('others', 'Others')
        )
        role_choices = (
            ('receptionist','Receptionist'),
            ('doctor','Doctor'),
            ('hospital_admin','Hospital Admin'),
            ('accounts','Accounts'),
            ('accounts_admin','Accounts Admin')
        )
        full_name = forms.CharField(
            label="Enter full name of the person to Invite",
            max_length=30,
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'name': 'username'}))
        gender = forms.ChoiceField(
            label="Gender",
            choices=gender_choices,
            widget=forms.Select,
        )
        email = forms.EmailField(
            label="Email ID to send invitation to",
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'name': 'email'}))
        mobile_number = forms.IntegerField(
            label = "Enter Mobile Number of the user",
            widget=forms.TextInput(
                attrs={
                    'type':'number',
                    'class': 'form-control',
                    'name': 'mobile_number'}))
        role = forms.ChoiceField(
            label="Role",
            choices=role_choices,
            widget=forms.Select,
        )
