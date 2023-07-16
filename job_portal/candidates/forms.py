from django.forms import ModelForm
from .models import Candidate, Resume


class CandidateProfileForm(ModelForm):
    # add more fields
    class Meta:
        model = Candidate
        fields = ["firstname", "lastname"]


class ResumeForm(ModelForm):
    # add more fields
    class Meta:
        model = Resume
        fields = ["graduation_Year", "file"]
