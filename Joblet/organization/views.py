from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Organization
# Create your views here.
def org_profile(request: HttpRequest, org_id):
    org = Organization.objects.get(pk = org_id)
    return render(request, 'org_profile.html', context={'org': org})
