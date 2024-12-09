from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Organization(models.Model):

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    approved = models.BooleanField(default=False)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
