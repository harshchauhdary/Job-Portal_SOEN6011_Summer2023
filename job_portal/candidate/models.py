from django.db import models


class App_user(models.Model):
    # add more fields
    firstname = models.CharField(max_length=255, null=True)
    lastname = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, unique=True, null=True)
    password = models.CharField(max_length=255, null=True)


class Job(models.Model):
    # add more fields
    position = models.CharField(max_length=255, null=True)


class Resume(models.Model):
    # add more fields
    graduation_Year = models.DateField(null=True)
    file = models.FileField(null=True, upload_to="files/")
