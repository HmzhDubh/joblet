from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Organization, Skill
from django.contrib.auth.models import User
# Create your views here.


def org_profile(request: HttpRequest, user_name):

    if 'edit' in request.GET:
        user = User.objects.get(username=user_name)
        org = Organization.objects.get(profile=user)
        print('Editing: '+request.GET['edit'])
        if 'name' in request.POST:

            org.name = request.POST['name']
            org.save()
            return redirect('organization:org_profile', user_name=user.username)

        if 'email' in request.POST:
            # print(request.POST['email'])
            org.email = request.POST['email']
            org.save()

        if 'phone_number' in request.POST:
            print(request.POST['phone_number'])
            org.phone_number = request.POST['phone_number']

        if 'location' in request.POST:
            print(request.POST['location'])
            org.location = request.POST['location']

        if 'website' in request.POST:
            print(request.POST['website'])
            org.website = request.POST['website']

        if 'linkedin' in request.POST:
            print(request.POST['linkedin'])
            org.linkedin = request.POST['linkedin']

        org.save()

    user = User.objects.get(username=user_name)
    org = Organization.objects.get(profile=user)
    return render(request, 'organization/org_profile.html', context={'org': org, 'skills': Skill.objects.all})


def add_skill(request: HttpRequest, skill_id):

    skill = Skill.objects.get(pk=skill_id)
    org = Organization.objects.get(profile=request.user)
    org.skills.add(skill)
    org.save()
    return redirect('organization:org_profile', user_name=request.user)


def remove_skill(request: HttpRequest, skill_id):

    skill = Skill.objects.get(pk=skill_id)
    org = Organization.objects.get(profile=request.user)
    org.skills.remove(skill)
    org.save()
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

        return redirect('organization:org_profile', user_name=request.user)

# def update_organization_profile(request: HttpRequest, user_name):
#
#     user = User.objects.get(username=user_name)
#     org = Organization.objects.get(profile=user)
#     if request.method == 'POST':
#         org.name = request.POST['name']
#         org.email = request.POST['email']
#         org.phone_number = request.POST['phone_number']
#         org.description = request.POST['description']
#         profile_completion = 50
#         org.save()
#     return render(request, 'organization/update_org.html', context={'org', org})
