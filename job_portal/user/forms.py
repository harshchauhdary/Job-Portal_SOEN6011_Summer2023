from django import forms
from .models import App_user


class UserProfileForm(forms.ModelForm):
    # add more fields
    class Meta:
        model = App_user
        fields = ["firstname", "lastname", "username", "password"]
        
        widgets = {
            "firstname": forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }

   
