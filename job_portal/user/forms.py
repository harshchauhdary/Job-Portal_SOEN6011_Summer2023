from django import forms
from .models import User


class UserProfileForm(forms.ModelForm):
    # add more fields
    class Meta:
        model = User
        fields = ["email", "role", "password"]

        widgets = {
            "email": forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }
