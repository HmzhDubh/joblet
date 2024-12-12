
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SignInForm
from django.db import transaction
from .models import Profile
from .models import Profile, Project, Education, Experince, Skill
from .forms import ProfileForm, ProjectForm, EducationForm, ExperinceForm, SkillForm
from django.urls import reverse
from organization.models import Organization
from django.contrib.auth.models import Group
from django.http import HttpRequest, HttpResponse
# Create your views here.


def signup_view(request: HttpRequest):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                login(request, user)
                if request.POST['acc_type'] == 'candidate':
                    my_group = Group.objects.get(name='candidate')
                    my_group.user_set.add(user)
                    # init the user profile todo
                elif request.POST['acc_type'] == 'organization':
                    my_group = Group.objects.get(name='organizations')
                    my_group.user_set.add(user)
                    # init the organization profile
                    new_organization = Organization(
                        profile = request.user,
                        email = request.POST['email']
                    )
                    new_organization.save()

            return redirect('main:home_view')

    else:
        form = SignUpForm()
    return render(request, 'accounts/sign_up.html', {'form': form})



def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  
                return redirect('main:home_view')
    else:
        form = SignInForm()
    return render(request, 'accounts/sign_in.html', {'form': form})

@login_required
def signout_view(request):
    logout(request)  

    return redirect('sign_in')  






@login_required
def profile_view(request, user_id):
    if request.user.id != user_id:
        return redirect('home')  

    profile = get_object_or_404(Profile, user_id=user_id)

    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            #messages.success(request, "Profile updated successfully!")

        skills_form = SkillForm(request.POST)
        if skills_form.is_valid():
            skill_name = skills_form.cleaned_data['skill_name']
            skill, created = Skill.objects.get_or_create(skill_name=skill_name)
            profile.skills.add(skill)
            profile.save()
            #messages.success(request, f"Skill '{skill_name}' added successfully!")

        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.profile = profile 
            project.save()
            #messages.success(request, "Project added successfully!")

        education_form = EducationForm(request.POST)
        if education_form.is_valid():
            education = education_form.save(commit=False)
            education.profile = profile  
            education.save()
            profile.save()
            #messages.success(request, "Education added successfully!")

     
        experience_form = ExperinceForm(request.POST)
        if experience_form.is_valid():
            experience = experience_form.save(commit=False)
            experience.profile = profile  
            experience.save()
            profile.save()
            # messages.success(request, "Experience added successfully!")

    
    projects = profile.projects.all()
    education = profile.education.all()
    experiences = profile.experience.all()
    skills = profile.skills.values_list('skill_name', flat=True)
    profile_form = ProfileForm(instance=profile)
    skills_form = SkillForm()
    project_form = ProjectForm()
    education_form = EducationForm()
    experience_form = ExperinceForm()

    return render(request, 'accounts/profile.html', {
        'profile_form': profile_form,
        'skills_form': skills_form,
        'project_form': project_form,
        'education_form': education_form,
        'experience_form': experience_form,
        'projects': projects,
        'education': education,
        'experiences': experiences,
        'skills': skills,
    })

    return redirect('accounts:signin')

