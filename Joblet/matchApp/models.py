from django.db import models
from candidate.models import Candidate
from organization.models import Organization
# Create your models here.


class Match(models.Model):

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class OrganizationLike(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_liked')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_likes')
    created_at = models.DateTimeField(auto_now_add=True)

class CandidateLike(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_liked')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_likes')
    created_at = models.DateTimeField(auto_now_add=True)

