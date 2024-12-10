from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SignInForm
from organization.models import Organization
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
    return redirect('accounts:signin')
