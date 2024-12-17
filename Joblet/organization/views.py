from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from candidate.views import check_and_create_match
from .forms import ProjectForm
from .models import Organization, Skill, Projects
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from candidate.models import Candidate

from matchApp.models import CandidateLike


 

# Create your views here.


def org_profile(request: HttpRequest, user_name):

    user = User.objects.get(username=user_name)
    org = Organization.objects.get(profile=user)

    if request.method == 'POST' and 'delete_project' in request.POST:
        if request.user.username == user_name:
            project_id = request.POST.get('delete_project')
            project = get_object_or_404(Projects, id=project_id, profile=org)
            project.delete()
            messages.success(request, 'Project deleted successfully.', 'alert-success')
            return redirect('organization:org_profile', user_name=user_name)
        else:
            messages.error(request, 'Only Profile owner can edit profile')

    if 'edit' in request.GET:
        if request.user.username == user_name:
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
        else:
            messages.error(request, 'Only Profile Owner can edit')
        
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


def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)

            org = request.user.organization.first()  
            
            if org:
                project.profile = org
                project.save()
                return redirect('organization:org_profile', user_name=request.user)
            else:
                messages.error(request, 'User does not have an associated organization.', 'alert-danger')
                return redirect('main:home_view')
        else:
            print('form is not valid')
    else:
        form = ProjectForm()

    return render(request, 'organization/add_project.html', {'form': form})


def update_project(request, project_id):
    project = get_object_or_404(Projects, id=project_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            project.delete()
            messages.success(request, 'Project deleted successfully.', 'alert-success')
            return redirect('organization:org_profile', user_name=request.user)
        
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            
            org = request.user.organization.first()
            
            if org:
                project.profile = org
                project.save()
                messages.success(request, 'Project updated successfully.', 'alert-success')
                return redirect('organization:org_profile', user_name=request.user)
            else:
                messages.error(request, 'User does not have an associated organization.', 'alert-danger')
                return redirect('main:home_view')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'organization/update_project.html', {'form': form, 'project': project})


def delete_project(request, project_id):
    project = get_object_or_404(Projects, id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('organization:profile', org_id=request.user.organization.id)
    return render(request, 'organization/delete_project.html', {'project': project})


def like_organization(request, organization_id):
    candidate = request.user.candidate  # Assuming candidate is tied to user
    organization = Organization.objects.get(id=organization_id)

    # Add the like
    CandidateLike.objects.get_or_create(candidate=candidate, organization=organization)

    # Check for a match
    check_and_create_match(organization, candidate)
    return redirect("main:home_view")
