from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import ProjectForm
from .models import Organization, Skill, Projects
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from candidate.models import Candidate
from matchApp.models import CandidateLike, OrganizationLike, Match
from candidate.views import check_and_create_match

 

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Organization, Skill
from .forms import OrganizationForm
from django.http import HttpRequest

def org_profile(request: HttpRequest, user_name):
    if request.user.username != user_name:
        messages.warning(request, 'You are not authorized to view this profile.', 'alert-danger')
        return redirect('main:home_view')

    user = get_object_or_404(User, username=user_name)
    org = get_object_or_404(Organization, profile=user)

    if request.method == 'POST':
        if 'edit' in request.POST:
            form = OrganizationForm(request.POST, request.FILES, instance=org)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!', 'alert-success')
                return redirect('organization:org_profile', user_name=user_name)
        elif 'delete_project' in request.POST:
            project_id = request.POST.get('delete_project')
            project = get_object_or_404(Projects, id=project_id, organization=org)
            project.delete()
            messages.success(request, 'Project deleted successfully.', 'alert-success')
            return redirect('organization:org_profile', user_name=user_name)

    else:
        form = OrganizationForm(instance=org)

    return render(request, 'organization/org_profile.html', context={
        'org': org,
        'form': form,
        'skills': Skill.objects.all()
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
        return_url = request.GET.get('next', request.path_info)
        messages.success(request, 'Skill was added Successfully', 'alert-success')
        return redirect(return_url)


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


from django.shortcuts import get_object_or_404
from django.contrib import messages


def like_organization(request, organization_id):
    candidate = request.user.candidate  # Assuming candidate is tied to the user
    organization = get_object_or_404(Organization, id=organization_id)

    try:
        # Check if the candidate has already liked the organization
        cand_like = CandidateLike.objects.filter(candidate=candidate, organization=organization).first()
        if cand_like:
            messages.info(request, 'You have already liked this organization.', 'alert-info')
        else:
            # Create a new like entry
            CandidateLike.objects.create(candidate=candidate, organization=organization)

            # Check for a match
            check_and_create_match(organization, candidate)
            messages.success(request, 'Liked successfully!', 'alert-success')

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred while liking the organization.', 'alert-danger')

    return redirect("main:home_view")

