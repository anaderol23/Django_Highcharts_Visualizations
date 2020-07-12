from django import forms
from django.contrib.auth.models import User
from lore_app.models import UserProfileInfo



class UserForm(forms.ModelForm): #base forms
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ("username", "email", "password")


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ("profile_pic",)
