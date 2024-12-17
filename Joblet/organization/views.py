from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Organization, Skill,OrganizationLike
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from candidate.models import CandidateLike,Candidate
from candidate.views import is_match
 
# Create your views here.


def org_profile(request: HttpRequest, user_name):

    if request.user.username != user_name:

        messages.warning(request, 'There is error uploading your profile', 'alert-danger')
        return redirect('main:home_view')

    user = User.objects.get(username=user_name)
    org = Organization.objects.get(profile=user)

    if 'edit' in request.GET:
        print('Editing: ' + request.GET['edit'])

        if 'name' in request.POST:

            if org.name == '':
                org.name = request.POST['name']
                org.profile_completion += 10
            else:
                org.name = request.POST['name']

        if 'logo' in request.FILES:
            if org.logo == '':

                org.logo = request.FILES['logo']
                org.profile_completion += 10
            else:
                org.logo = request.FILES['logo']

        if 'email' in request.POST:
            if org.email == '':
                org.email = request.POST['email']
                org.profile_completion += 10
            else:
                org.email = request.POST['email']
                print("Edit email")

        if 'phone_number' in request.POST:
            if org.phone_number == '':
                org.phone_number = request.POST['phone_number']
                org.profile_completion += 10
            else:
                org.phone_number = request.POST['phone_number']

        if 'location' in request.POST:
            if org.location == '':

                org.location = request.POST['location']
                org.profile_completion += 10
            else:
                org.location = request.POST['location']

        if 'website' in request.POST:
            if org.website == '':
                org.website = request.POST['website']
                org.profile_completion += 10
            else:
                org.website = request.POST['website']

        if 'linkedin' in request.POST:
            if org.linkedin == '':
                org.linkedin = request.POST['linkedin']
                org.profile_completion += 10
            else:
                org.linkedin = request.POST['linkedin']

        if 'description' in request.POST:
            if org.description == '':
                org.description = request.POST['description']
                org.profile_completion += 10
            else:
                org.description = request.POST['description']

        if 'job_title' in request.POST:
            if org.job_title == '':
                org.job_title = request.POST['job_title']
                org.profile_completion += 10
            else:
                org.job_title = request.POST['job_title']

        org.save()
        messages.success(request, 'Profile was updated Successfully', 'alert-success')

    return render(request, 'organization/org_profile.html', context={
        'org': org,
        'skills': Skill.objects.all
    })


def add_skill(request: HttpRequest, skill_id):

    skill = Skill.objects.get(pk=skill_id)
    org = Organization.objects.get(profile=request.user)
    org.skills.add(skill)
    if not org.profile_completion >= 100:
        org.profile_completion += 3
    org.save()
    messages.success(request, 'Skill was added Successfully', 'alert-success')
    return redirect('organization:org_profile', user_name=request.user)


def remove_skill(request: HttpRequest, skill_id):

    skill = Skill.objects.get(pk=skill_id)
    org = Organization.objects.get(profile=request.user)
    org.skills.remove(skill)
    org.profile_completion -= 3
    org.save()
    messages.warning(request, 'Skill was removed Successfully', 'alert-warning')
    return redirect('organization:org_profile', user_name=request.user)


def new_skill_view(request: HttpRequest):

    if request.method == 'POST':
        new_skill = Skill(
            skill_name = request.POST['skill_name']
        )
        new_skill.save()

        org = Organization.objects.get(profile=request.user)
        org.skills.add(new_skill)
        org.save()
        messages.success(request, 'Skill was added Successfully', 'alert-success')
        return redirect('organization:org_profile', user_name=request.user)


def change_org_status(request: HttpRequest, org_id):
    org = Organization.objects.get(pk=org_id)
    if request.user.is_superuser:
        org.approved = not org.approved
        org.save()
        messages.success(request, 'Organization Status Updated successfully', 'alert-success')
    return redirect('dashboard:dashboard_view')

def like_organization(request, organization_id):
    """
    Allow a candidate to like an organization. Check for a match if mutual likes exist.
    """
    # Fetch the organization and candidate objects
    organization = get_object_or_404(Organization, id=organization_id)
    candidate = get_object_or_404(Candidate, user=request.user)

    # Toggle the like
    like, created = CandidateLike.objects.get_or_create(user=request.user, organization=organization)
    if not created:
        like.delete()  # Remove the like if it already exists
    else:
        # Check for mutual like (match)
        if is_match(candidate, organization):
            messages.success(request, f"It's a match! You and {organization.name} like each other.")
    
    # Redirect to the homepage
    return redirect("main:home_view")


