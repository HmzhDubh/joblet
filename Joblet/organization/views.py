from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Organization
from django.contrib.auth.models import User
# Create your views here.

def org_profile(request: HttpRequest, user_name):
    user = User.objects.get(username=user_name)
    org = Organization.objects.get(profile=user)
    return render(request, 'organization/org_profile.html', context={'org': org})
def update_profile(request: HttpRequest, user_name):

    user = User.objects.get(username=user_name)
    org = Organization.objects.get(profile=user)
    if request.method == 'POST':
        org.name = request.POST['name']
        org.email = request.POST['email']
        org.phone_number = request.POST['phone_number']
        org.description = request.POST['description']
        profile_completion = 50
        org.save()
    return render(request, 'organization/update_org.html', context={'org', org})