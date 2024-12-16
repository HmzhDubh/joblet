from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.db import transaction, IntegrityError
from django.urls import reverse

from organization.models import Organization
from candidate.models import Candidate

# Create your views here.


def candidate_signup_view(request: HttpRequest):

    if request.method == "POST":
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    email = request.POST['email'],
                    password = request.POST['password'],
                    username = request.POST['username'],
                )
                new_user.save()
                my_group = Group.objects.get(name='candidate')
                my_group.user_set.add(new_user)

                candidate_profile = Candidate(
                    user = new_user,
                    about = request.POST['about'],
                    avatar = request.FILES.get("avatar", Candidate._meta.get_field("avatar").get_default()),
                )
                candidate_profile.save()
            login(request, new_user)
            messages.success(request, f'{new_user.username} Account was created Successfully', 'alert-success')

            return redirect(f'{reverse("main:home_view")}?type=candidate')
        except IntegrityError as ie:
            print(ie)
            messages.error(request, 'This username is taken, please try another one', 'alert-danger')
        except Exception as e:
            print(e)
            messages.error(request, 'error in creating your account', 'alert-danger')

    return render(request, 'accounts/sign_up.html')


def organization_signup_view(request: HttpRequest):

    if request.method == "POST":
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(

                    password = request.POST['password'],
                    username = request.POST['username'],
                )
                new_user.save()
                my_group = Group.objects.get(name='organizations')
                my_group.user_set.add(new_user)

                organization_profile = Organization(

                    profile = new_user,
                    name = request.POST['name'],
                    email = request.POST['email'],
                    description = request.POST['about'],
                    logo = request.FILES.get("logo", Organization._meta.get_field("logo").get_default()),
                )
                organization_profile.save()

            login(request, new_user)
            messages.success(request, f'{new_user.username} Account was created Successfully', 'alert-success')

            return redirect(f'{reverse("main:home_view")}?type=candidate')
        except IntegrityError as ie:
            print(ie)
            messages.error(request, 'This username is taken, please try another one', 'alert-danger')
        except Exception as e:
            print(e)
            messages.error(request, 'error in creating your account', 'alert-danger')

    return render(request, 'accounts/sign_up.html')


def signin_view(request: HttpRequest):

    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            messages.success(request, f'{user.username} Signed in Successfully', 'alert-success')
            return redirect(f'{reverse("main:home_view")}?type=candidate')
        else:
            messages.error(request, 'Username or password is wrong, please try again', 'alert-danger')
    return render(request, 'accounts/sign_in.html')


@login_required
def signout_view(request):
    logout(request)  

    return redirect('accounts:signin')

