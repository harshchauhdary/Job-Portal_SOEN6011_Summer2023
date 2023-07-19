from django import forms
from .models import Resume, Candidate
from django.core.validators import MinLengthValidator, MaxLengthValidator


class ResumeForm(forms.ModelForm):
    # add more fields
    class Meta:
        model = Resume
        fields = ["summary", "education",
                  "experience", "skills", "file"]

        widgets = {
            "summary": forms.TextInput(attrs={'class': 'form-control'}),
            "education": forms.TextInput(attrs={'class': 'form-control'}),
            "experience": forms.TextInput(attrs={'class': 'form-control'}),
            "skills": forms.TextInput(attrs={'class': 'form-control'}),
            "fileName": forms.TextInput(attrs={'class': 'form-control'}),
            "file": forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the 'required' attribute of the 'file' field to False
        self.fields["file"].required = False


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["firstName", "lastName", "phone"]
        widgets = {
            "firstName": forms.TextInput(attrs={'class': 'form-control'}),
            "lastName": forms.TextInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or not (10 <= len(phone) <= 15):
            raise forms.ValidationError("Phone number must be a 10-15 digit number.")
        return phone
    
