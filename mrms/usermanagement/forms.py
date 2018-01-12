# log/forms.py
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from django import forms

from usermanagement.models import User

# If you don't do this you cannot use Bootstrap CSS


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=" ",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'username',
                'placeholder':"Mobile number"
                }))
    password = forms.CharField(
        label=" ",
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'name': 'username',
                'password': forms.PasswordInput(),
                'placeholder':"Enter your password"
                }))


class SignUpForm(UserCreationForm):
    gender_choices = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    )
    username = forms.CharField(
        label="Mobile Number +91",
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

    dob = forms.DateField(
        label="Date Of Birth",
        widget=forms.DateInput(
            format=('%d/%m/%Y'),
            attrs={
                'class': 'form-control datepicker',
                'name': 'username',
                'placeholder': 'yyyy-mm-dd'}))
    full_name = forms.CharField(
        label="Enter your full name",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'username'}))

    def clean(self):
        if len(self.cleaned_data.get('username')) != 10:
            raise forms.ValidationError(
                "Mobile Number cannot be less than 10 digits")
        print(self.cleaned_data)
        return self.cleaned_data

    class Meta(UserCreationForm.Meta):
        model = User


class DoctorProfileForm(forms.ModelForm):
    doctor_date_of_reg = forms.DateField(
        label="Date of Registration",
        widget=forms.DateInput(
            format=('%d/%m/%Y'),
            attrs={
                'class': 'form-control datepicker',
            }))

    class Meta:
        model = User
        fields = [
            "experience",
            "doctor_available_time",
            "doctor_registration_number",
            "doctor_state_medical_council",
            "doctor_date_of_reg",
            "doctor_bio",
            "doctor_specialization"
        ]

    def __init__(self, *args, **kwargs):
        super(DoctorProfileForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        cd["is_doctor"] = True
        cd["doctor_activated"] = True
        return cd
