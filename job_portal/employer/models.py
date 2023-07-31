from django.db import models
from user.models import User


class Employer(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=255)
    companyEmail = models.EmailField()
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

class Job(models.Model):
    position=models.CharField(max_length=255)
    description = models.TextField()
    applicationDeadline = models.DateField()
    status=models.CharField(max_length=255)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

    def get_job_message(self):
        return f"Position: {self.position}, Description: {self.description}"