# from django.forms import ModelForm
# from .models import Resume, Job

# class JobForm(ModelForm):
#     # add more fields
#     class Meta:
#         model = Job
#         fields = ["position"]
from django import forms
from .models import Job, Employer


class JobForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSE', 'Close'),
    )

    class Meta:
        model = Job
        fields = ('position', 'description', 'applicationDeadline', 'status')
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Job Description'}),
            'applicationDeadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Job Status'  # Customize the label here
    )

    position = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Position'  # Customize the label here
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Job Description'}),
        label='Description'  # Customize the label here
    )

    applicationDeadline = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Application Deadline'  # Customize the label here
    )




class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('companyName', 'companyEmail', 'firstName', 'lastName', 'phone')
        widgets = {
            "firstName": forms.TextInput(attrs={'class': 'form-control'}),
            "lastName": forms.TextInput(attrs={'class': 'form-control'}),
            "companyName": forms.TextInput(attrs={'class': 'form-control'}),
            "companyEmail": forms.TextInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_companyEmail(self):
        email = self.cleaned_data.get('companyEmail')
        if not forms.EmailField().clean(email):
            raise forms.ValidationError("Invalid email format.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or not (10 <= len(phone) <= 15):
            raise forms.ValidationError("Phone number must be a 10-15 digit number.")
        return phone