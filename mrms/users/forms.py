# log/forms.py
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from django import forms

# If you don't do this you cannot use Bootstrap CSS


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Mobile Number",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'username'}))


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
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'username'}))
    dob = forms.DateField(
        label="Date Of Birth",
        widget=forms.DateInput(
            format=('%d/%m/%Y'),
            attrs={
                'class': 'form-control',
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
        return self.cleaned_data
