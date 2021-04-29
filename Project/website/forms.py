from django import forms
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    restaurantname = forms.CharField(label='Restaurant Name',max_length=50, required=True)
    username = forms.CharField(label='username', max_length=50, required=True)
    password1 = forms.CharField(label='password', max_length=50, required=True)
    password2 = forms.CharField(label='password*', max_length=50, required=True)

class LoginForm(forms.Form):
    restaurantname = forms.CharField(label='Restaurant Name',max_length=50, required=True)
    username = forms.CharField(label='username', max_length=50, required=True)
    password = forms.CharField(label='password', max_length=50, required=True)


    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     password1 = cleaned_data.get("password1")
    #     password2 = cleaned_data.get("password2")
    #     if password1 != password2:
    #         raise forms.ValidationError("Passwords do not match")
        
    #     return cleaned_data



    
#	fields = form ["restaurant name", "username", "password1", "password2"]