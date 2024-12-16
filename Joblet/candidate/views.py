from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidate, Project, Education, Experince, CandidateLike
from django.http import JsonResponse
from organization.models import Skill, Organization

# Create your views here.


@login_required
def candidate_profile_view(request, user_name):

    if request.user.username != user_name:

        messages.warning(request, 'There is error uploading your profile', 'alert-danger')
        return redirect('main:home_view')

    user = User.objects.get(pk=request.user.id)
    candidate_profile = Candidate.objects.get(user=user.id)

    if request.method == 'POST':

        if 'about' in request.POST:
            candidate_profile.about = request.POST['about']

        if 'first_name' in request.POST:
            user.first_name = request.POST['first_name']

        if 'last_name' in request.POST:
            user.last_name = request.POST['last_name']

        if 'avatar' in request.FILES: candidate_profile.avatar = request.FILES['avatar']

        messages.success(request, 'profile updates successfully', 'alert-success')
        candidate_profile.save()

    return render(request, 'candidate/candidate_profile.html', {
        'candidate_profile': candidate_profile,
        'skills': Skill.objects.all(),
        'degree_choices': Education.DEGREE_CHOICES,

    })


def add_skill(request: HttpRequest):

    skill = Skill.objects.get(pk=request.POST['skill'])
    candidate = Candidate.objects.get(user=request.user)
    candidate.skills.add(skill)
    if not candidate.profile_completion >= 100:
        candidate.profile_completion += 5
    candidate.save()
    messages.success(request, 'Skill was added Successfully', 'alert-success')
    return redirect('candidate:candidate_profile_view', user_name=request.user)


def remove_skill(request: HttpRequest, skill_id):
    try:
        skill = Skill.objects.get(pk=skill_id)
        candidate = Candidate.objects.get(user=request.user)
        candidate.skills.remove(skill)
        candidate.profile_completion -= 5
        candidate.save()
        messages.warning(request, 'Skill was removed Successfully', 'alert-warning')

    except Exception as e:

        print(e)
        messages.error(request, 'Error Deleting record', 'alert-danger')

    return redirect('candidate:candidate_profile_view', user_name=request.user)


def add_project(request: HttpRequest):

    with transaction.atomic():
        candidate = Candidate.objects.get(user=request.user)
        project = Project(
            profile = candidate,
            title = request.POST['title'],
            description = request.POST['description'],
            tools_used =request.POST['tools_used'],
        )
        project.save()

        if not candidate.profile_completion >= 100:
            candidate.profile_completion += 20

        candidate.save()

        messages.success(request, 'Project was added Successfully', 'alert-success')
    return redirect('candidate:candidate_profile_view', user_name=request.user)


def remove_project(request: HttpRequest, project_id):
    try:
        project = Project.objects.get(pk=project_id)
        project.delete()

        candidate = Candidate.objects.get(user=request.user)
        candidate.profile_completion -= 20
        candidate.save()

        messages.warning(request, 'Project was removed Successfully', 'alert-warning')
    except Exception as e:
        print(e)
        messages.error(request, 'Error Deleting record', 'alert-danger')

    return redirect('candidate:candidate_profile_view', user_name=request.user)


def add_education(request: HttpRequest):

    with transaction.atomic():
        candidate = Candidate.objects.get(user=request.user)
        education = Education(
            profile=candidate,
            university=request.POST['university'],
            degree=request.POST['degree'],
            major=request.POST['major'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            GPA=float(request.POST['GPA']),
            certificate=request.POST['certificate']
        )

        # Save the education record
        education.save()

        if not candidate.profile_completion >= 100:
            candidate.profile_completion += 25

        candidate.save()

        messages.success(request, 'Project was added Successfully', 'alert-success')
    return redirect('candidate:candidate_profile_view', user_name=request.user)


def remove_education(request: HttpRequest, education_id):
    try:
        edu = Education.objects.get(pk=education_id)
        edu.delete()

        candidate = Candidate.objects.get(user=request.user)
        candidate.profile_completion -= 25
        candidate.save()

        messages.warning(request, 'Education was removed Successfully', 'alert-warning')

    except Experince as e:
        print(e)
        messages.error(request, 'Error Deleting record', 'alert-danger')

    return redirect('candidate:candidate_profile_view', user_name=request.user)


def add_experience(request: HttpRequest):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                candidate = Candidate.objects.get(user=request.user)
                experience = Experince(
                    profile=candidate,
                    company=request.POST['company'],
                    position=request.POST['position'],
                    start_date=request.POST['start_date'],
                    end_date=request.POST['end_date']
                )

                # Save the education record
                experience.save()

                if not candidate.profile_completion >= 100:
                    candidate.profile_completion += 25

                candidate.save()

            messages.success(request, 'Experience added successfully!', 'alert-success')
            return redirect('candidate:candidate_profile_view', user_name=request.user)
        except Experince as e:
            print(e)
            messages.error(request, 'Error adding Experience', 'alert-danger')

    return redirect('candidate:candidate_profile_view', user_name=request.user)


def remove_experience(request: HttpRequest, experience_id):
    try:
        exp = Experince.objects.get(pk=experience_id)
        exp.delete()

        candidate = Candidate.objects.get(user=request.user)
        candidate.profile_completion -= 25
        candidate.save()

        messages.warning(request, 'Education was removed Successfully', 'alert-warning')


    except Experince as e:
        print(e)
        messages.error(request, 'Error Deleting record', 'alert-danger')

    return redirect('candidate:candidate_profile_view', user_name=request.user)


def change_candidate_status(request: HttpRequest, candidate_id):
    candidate = Candidate.objects.get(pk=candidate_id)
    if request.user.is_superuser:
        candidate.approved = not candidate.approved
        candidate.save()
        messages.success(request, 'Candidate Status Updated successfully', 'alert-success')
    return redirect('dashboard:dashboard_view')

def like_candidate(request, candidate_id):
    # Get the candidate object or return 404 if not found
    candidate = get_object_or_404(Candidate, id=candidate_id)
    
    # Toggle the like
    like, created = CandidateLike.objects.get_or_create(user=request.user, candidate=candidate)
    if not created:
        like.delete()  # If the like already exists, remove it (unlike)
    
    # Redirect back to the previous page or fallback to home if no referrer
    return redirect("main:home_view")
