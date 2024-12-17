from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Skill(models.Model):
    skill_name = models.CharField(max_length=50)


class Organization(models.Model):

    profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization')

    name = models.CharField(max_length=150, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True)
    job_title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    location = models.TextField(null=True)
    website = models.URLField(null=True)
    linkedin = models.URLField(null=True)
    logo = models.ImageField(upload_to='images', default='images/logo.jpg')
    skills = models.ManyToManyField(Skill)
    approved = models.BooleanField(default=False)
    profile_completion = models.SmallIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)


class Projects(models.Model):

    profile = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="project")
    title = models.CharField(max_length=200)
    description = models.TextField()
    tools_used = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


