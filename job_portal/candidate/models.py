from django.db import models

from user.models import User


class Job(models.Model):
    pos = models.CharField(max_length=255)


class Resume(models.Model):
    # add more fields
    fileName = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)
    file = models.FileField(null=True, upload_to="files/")


class Candidate(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    resume = models.ForeignKey(
        Resume, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
