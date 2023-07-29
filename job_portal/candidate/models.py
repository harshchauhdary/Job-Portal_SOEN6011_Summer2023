from django.db import models

from user.models import User
from employer.models import Job


class Resume(models.Model):
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


class Application(models.Model):
    candidate = models.ForeignKey(
        Candidate, on_delete=models.SET_NULL, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)


class Tracking(models.Model):
    date = models.DateField()
