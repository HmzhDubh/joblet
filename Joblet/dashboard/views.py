from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from main.models import Contact
from organization.models import Organization, Skill
from candidate.models import Candidate


# Create your views here.
def dashboard_view(request: HttpRequest):
    orgs = Organization.objects.all()
    contact_messages = Contact.objects.all()
    skills = Skill.objects.all()
    candidates = Candidate.objects.all()
    return render(request, 'dashboard/dashboard.html', context={'candidates':candidates, 'contact_messages': contact_messages, 'orgs':orgs, 'skills':skills})