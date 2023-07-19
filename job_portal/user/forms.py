from django import forms
from .models import User


class UserProfileForm(forms.ModelForm):
    # add more fields
    class Meta:
        model = User
        fields = ["email", "role", "password"]

        widgets = {
            "email": forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            "role": forms.Select(attrs={'class': 'form-select'}),
        }

        # Choices for the role field
    ROLE_CHOICES = (
        ('E', 'Employer'),
        ('C', 'Candidate'),
    )

    # Overriding the 'role' field to use CharField with choices
    role = forms.CharField(
        widget=forms.Select(choices=ROLE_CHOICES, attrs={'class': 'form-select'})
    )
