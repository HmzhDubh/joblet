from django.db import models
from candidate.models import Candidate
from organization.models import Organization, Projects
# Create your models here.

class CandidateLike(models.Model):

    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='org_liked')
    can = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidates_likes')
    created_at = models.DateTimeField(auto_now_add=True)

class OrganizationLike(models.Model):

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_liked')
    organization = models.ForeignKey(Organization, default=0, on_delete=models.CASCADE, related_name='organization_likes')
    created_at = models.DateTimeField(auto_now_add=True)


class Match(models.Model):

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

