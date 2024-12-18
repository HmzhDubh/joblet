from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from matchApp.models import CandidateSuperLike, OrganizationSuperLike
from candidate.models import Candidate
from organization.models import Organization


# Create your views here.


def candidate_super_like(request: HttpRequest, candidate_id):
    """
    Organization gives candidates a Super Like
    :param request:
    :param candidate_id:
    :return:
    """

    organization = request.user.organization  # Assuming candidate is tied to user
    candidate = Candidate.objects.get(id=candidate_id)

    candidate_super_ike, created = CandidateSuperLike.objects.get_or_create(organization=organization, candidate=candidate)
    if created:
        messages.success(request, 'Super liked !!!', 'alert-success')
        print("Super Like created!")
    else:
        messages.error(request, 'Super Liked already.', 'alert-danger')
        print("Super Liked already.")

    return redirect("main:home_view")

def organization_super_like(request: HttpRequest, organization_id):
    """
       Candidates give Organizations a Super Like
       :param request:
       :param candidate_id:
       :return:
       """

    organization = Organization.objects.get(id=organization_id)  # Assuming candidate is tied to user
    candidate = request.user.candidate

    organization_super_ike, created = OrganizationSuperLike.objects.get_or_create(organization=organization, candidate=candidate)

    if created:
        messages.success(request, 'Super liked !!!', 'alert-success')
        print("Super Like created !!!")
    else:
        messages.error(request, 'Super Liked already.', 'alert-danger')
        print("Super Liked already.")

    return redirect("main:home_view")