from django import forms
from .models import Resume, Candidate


class ResumeForm(forms.ModelForm):
    # add more fields
    class Meta:
        model = Resume
        fields = ["summary", "education",
                  "experience", "skills", "file"]

        widgets = {

            "file": forms.FileInput(attrs={'class': 'form-control'}),
        }


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["firstName", "lastName", "phone"]
    widgets = {

        "firstName": forms.FileInput(attrs={'class': 'form-control'}),
    }
