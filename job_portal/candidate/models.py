from django.db import models

from user.models import User
from employer.models import Job

class Resume(models.Model):
    summary = models.CharField(max_length=255)
    file = models.FileField(null=True, upload_to="files/")


class Education(models.Model):
    resume = models.ForeignKey(Resume, related_name='educations', on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()


class Experience(models.Model):
    resume = models.ForeignKey(Resume, related_name='experiences', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Project(models.Model):
    resume = models.ForeignKey(Resume, related_name='projects', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()


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

