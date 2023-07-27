from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    # overriding the save method so that when we update password through aadmin panel, it gets hashed
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
