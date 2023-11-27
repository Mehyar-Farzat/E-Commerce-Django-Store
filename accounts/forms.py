from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):     # create signup form and inherit from UserCreationForm 
    class Meta:
        model = User                   # set model to User model
        fields = ['username','email','password1','password2']    # set fields to username, email, password1, password2


class ActivationForm(forms.Form):         # create activation form 
    code = forms.CharField(max_length=10)      # add code field to form 