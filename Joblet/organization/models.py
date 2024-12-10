from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Organization(models.Model):

    name = models.CharField(max_length=150, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True)
    logo = models.ImageField(upload_to='images', default='images/logo.jpg')
    approved = models.BooleanField(default=False)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_completion = models.SmallIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)