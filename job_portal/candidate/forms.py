from django import forms
from .models import Resume


class ResumeForm(forms.ModelForm):
    # add more fields
    class Meta:
        model = Resume
        fields = ["graduation_Year", "file"]

        widgets = {
            "graduation_Year": forms.DateInput(attrs={'class': 'form-control'}),
            "file": forms.FileInput(attrs={'class': 'form-control'}),
        }
