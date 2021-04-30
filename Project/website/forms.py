from django import forms
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    restaurantname = forms.CharField(label='Restaurant Name',max_length=50, required=True)
    username = forms.CharField(label='username', max_length=50, required=True)
    password1 = forms.CharField(label='password', max_length=50, required=True)
    password2 = forms.CharField(label='password*', max_length=50, required=True)

class AddMenuItemForm(forms.Form):
    menuitemname = forms.CharField(label='menuitemname',max_length=50, required=True)
    menuitemdescription = forms.CharField(label='menuitemdescription', max_length=50, required=True)
    menuitemprice = forms.FloatField(label='menuitemprice', required=True)

class UpdateMenuItemNameForm(forms.Form):
    menuitemname = forms.CharField(label='menuitemname',max_length=50, required=True)

class UpdateMenuItemDescriptionForm(forms.Form):
    menuitemdescription = forms.CharField(label='menuitemdescription', max_length=500, required=True)

class UpdateMenuItemPriceForm(forms.Form):
    menuitemprice = forms.FloatField(label='menuitemprice', required=True)
    
class LoginForm(forms.Form):
    restaurantname = forms.CharField(label='Restaurant Name',max_length=50, required=True)
    username = forms.CharField(label='username', max_length=50, required=True)
    password = forms.CharField(label='password', max_length=50, required=True)

class SearchForm(forms.Form):
    restaurantsearch = forms.CharField(label='Restaurant Name',max_length=50, required=True)



    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     password1 = cleaned_data.get("password1")
    #     password2 = cleaned_data.get("password2")
    #     if password1 != password2:
    #         raise forms.ValidationError("Passwords do not match")
        
    #     return cleaned_data



    
#	fields = form ["restaurant name", "username", "password1", "password2"]