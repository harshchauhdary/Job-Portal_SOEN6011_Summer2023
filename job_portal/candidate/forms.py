from django.forms import ModelForm
from .models import Resume


class ResumeForm(ModelForm):
    # add more fields
    class Meta:
        model = Resume
        fields = ["graduation_Year", "file"]
