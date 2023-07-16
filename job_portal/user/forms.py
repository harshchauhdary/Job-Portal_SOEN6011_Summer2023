from django.forms import ModelForm
from .models import User


class UserProfileForm(ModelForm):
    # add more fields
    class Meta:
        model = User
        fields = ["firstname", "lastname"]
