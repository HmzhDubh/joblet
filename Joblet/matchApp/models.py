from django.db import models
from candidate.models import Candidate
from organization.models import Organization, Projects
# Create your models here.


class Match(models.Model):

    candidate = models.ManyToManyField(Candidate)
    project = models.ManyToManyField(Projects)
    created_at = models.DateTimeField(auto_now_add=True)

