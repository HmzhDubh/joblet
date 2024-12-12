from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from main.models import Contact
from organization.models import Organization, Skill


# Create your views here.
def dashboard_view(request: HttpRequest):
    orgs = Organization.objects.all()
    contact_messages = Contact.objects.all()
    skills = Skill.objects.all()
    return render(request, 'dashboard/dashboard.html', context={'contact_messages': contact_messages, 'orgs':orgs, 'skills':skills})