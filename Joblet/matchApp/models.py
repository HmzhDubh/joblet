from django.db import models
from candidate.models import Candidate
from organization.models import Organization
# Create your models here.


class Match(models.Model):

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Match Between {self.candidate.user.first_name} And {self.organization.name}'

class OrganizationLike(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_liked')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'ORG:{self.organization.name} Liked CAN:{self.candidate.user.first_name}'

class CandidateLike(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_liked')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'CAN:{self.candidate.user.first_name} Liked ORG:{self.organization.name}'

class CandidateSuperLike(models.Model):

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class OrganizationSuperLike(models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)