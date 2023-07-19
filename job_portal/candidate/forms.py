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
        min_length = 10  # Minimum phone number length
        max_length = 15  # Maximum phone number length

        # Use MinLengthValidator and MaxLengthValidator to validate the phone number length
        validators = [MinLengthValidator(min_length), MaxLengthValidator(max_length)]

        for validator in validators:
            try:
                validator(phone)
            except forms.ValidationError as e:
                raise forms.ValidationError("Phone number must be between 10 and 15 digits.")

        return phone
