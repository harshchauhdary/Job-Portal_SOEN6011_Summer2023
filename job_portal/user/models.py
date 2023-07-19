from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
