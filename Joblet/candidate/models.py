from django.db import models
from django.contrib.auth.models import User
from organization.models import Skill


# Create your models here.


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    profile_completion = models.SmallIntegerField(default=10)
    avatar = models.ImageField(upload_to="images/avatars/", default="images/avatars/default.webp")
    skills = models.ManyToManyField(Skill)
    website = models.URLField(null=True)
    github = models.URLField(null=True)
    linkedin = models.URLField(null=True)



    def __str__(self):
        return f"{self.user.username}'s Profile"


class Project(models.Model):

    profile = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=200)
    description = models.TextField()
    tools_used = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Education(models.Model):

    DEGREE_CHOICES = [
        ('HIGH_SCHOOL', 'High School'),
        ('ASSOCIATE', 'Associate Degree'),
        ('BACHELOR', 'Bachelor\'s Degree'),
        ('MASTER', 'Master\'s Degree'),
        ('PHD', 'Doctorate/PhD'),
        ('DIPLOMA', 'Diploma'),
        ('CERTIFICATION', 'Certification'),
        ('OTHER', 'Other'),
    ]

    profile = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="education")
    start_date = models.DateField()
    end_date = models.DateField()
    university = models.CharField(max_length=200)
    major = models.CharField(max_length=100, default='none')
    GPA = models.FloatField(default=5.0)
    degree = models.CharField(max_length=100, choices=DEGREE_CHOICES, default='Other')
    certificate = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.university

class Experince(models.Model):
    profile = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="experience")
    start_date = models.DateField()
    end_date = models.DateField()
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.position} at {self.company}"
    








