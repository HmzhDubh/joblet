from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Skill(models.Model):
    skill_name = models.CharField(max_length=50)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="images/avatars/", default="images/avatars/default.webp")
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return f"{self.user.username}'s Profile"





class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=200)
    description = models.TextField()
    tools_used = models.TextField(blank=True)
    created_at = models.DateField()  

    def __str__(self):
        return self.title
    

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="education")
    start_date = models.DateField()  
    end_date = models.DateField()
    university = models.CharField(max_length=200)
    certificate = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.university

class Experince(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="experience")
    start_date = models.DateField()  
    end_date = models.DateField()  
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.position} at {self.company}"

