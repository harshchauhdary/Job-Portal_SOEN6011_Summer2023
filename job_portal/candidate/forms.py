from django import forms
from django.forms import inlineformset_factory
from .models import Resume, Candidate, Education, Experience, Skill, Project
from django.core.validators import MinLengthValidator, MaxLengthValidator

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ["school_name", "degree", "start_date", "end_date"]
        widgets = {
            "school_name": forms.TextInput(attrs={'class': 'form-control'}),
            "degree": forms.TextInput(attrs={'class': 'form-control'}),
            "start_date": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "end_date": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

EducationFormSet = inlineformset_factory(Resume, Education, form=EducationForm, extra=0)

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
        }

SkillFormSet = inlineformset_factory(Resume, Skill, form=SkillForm, extra=0)

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ["company_name", "position", "start_date", "end_date", 'description']
        widgets = {
            "company_name": forms.TextInput(attrs={'class': 'form-control'}),
            "position": forms.TextInput(attrs={'class': 'form-control'}),
            "start_date": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "end_date": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows': 3, 'placeholder': 'Bullet point 1\nBullet point 2\nBullet point 3'}),
        }

ExperienceFormSet = inlineformset_factory(Resume, Experience, form=ExperienceForm, extra=0)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "start_date", "end_date", "description"]
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "start_date": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "end_date": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "description": forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Bullet point 1\nBullet point 2\nBullet point 3'}),
        }

ProjectFormSet = inlineformset_factory(Resume, Project, form=ProjectForm, extra=0)

class ResumeForm(forms.ModelForm):
    # add more fields
    class Meta:
        model = Resume
        # fields = ["summary", "education",
        #           "experience", "skills", "file"]
        fields = ["summary", "file"]

        # widgets = {
        #     "summary": forms.TextInput(attrs={'class': 'form-control'}),
        #     "education": forms.TextInput(attrs={'class': 'form-control'}),
        #     "experience": forms.TextInput(attrs={'class': 'form-control'}),
        #     "skills": forms.TextInput(attrs={'class': 'form-control'}),
        #     "fileName": forms.TextInput(attrs={'class': 'form-control'}),
        #     "file": forms.FileInput(attrs={'class': 'form-control'}),
        # }
        widgets = {
            "summary": forms.TextInput(attrs={'class': 'form-control'}),
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
    
