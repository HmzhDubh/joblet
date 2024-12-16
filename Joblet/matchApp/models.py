from django.db import models
from candidate.models import Candidate
from organization.models import Organization, Projects
# Create your models here.


class Match(models.Model):

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

