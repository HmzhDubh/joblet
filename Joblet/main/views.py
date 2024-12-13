from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import ContactForm
from organization.models import Organization
from candidate.models import Candidate

# Create your views here.

def home_view(request:HttpRequest):

    orgs = Organization.objects.all()
    total_orgs = len(orgs)
    carousel_items = []
    if total_orgs > 0:

        # Get the current active index (could be from query params or session)
        active_index = int(request.GET.get('active', 0))

        # Calculate previous and next indices with wrap-around
        prev_index = (active_index - 1) % total_orgs
        next_index = (active_index + 1) % total_orgs

        # Create a list of organizations with their position classes
        carousel_items = []


        for i, org in enumerate(orgs):
            if i == active_index:
                position_class = 'active'
            elif i == prev_index:
                position_class = 'left'
            elif i == next_index:
                position_class = 'right'
            else:
                continue  # Skip organizations that aren't adjacent to the active one

            carousel_items.append({
                'org': org,
                'position_class': position_class
            })
        else:
            carousel_items = []

    for group in request.user.groups.all():
        if group.name == 'organization':
            if request.user.is_authenticated and not request.user.is_superuser:
                user_org = Organization.objects.get(profile=request.user)
                if user_org.profile_completion <= 80:
                    messages.warning(request, 'your profile is not complete please complete it to continue', 'alert-warning')
            else:
                user_org = []
        elif group.name == 'candidate':
            if request.user.is_authenticated:
                user_candidate = Candidate.objects.get(user=request.user)
                if user_candidate.profile_completion <= 80:
                    messages.warning(request, 'your profile is not complete please complete it to continue', 'alert-warning')
            else:
                user_candidate = []
        else:  # guest / admin
            user_org = []
            user_candidate = []

    return render(request,"main/home.html", context={'orgs': orgs, 'carousel_items': carousel_items, 'total_orgs': total_orgs})


def contact_view(request: HttpRequest):

    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Yous message was sent successfully', 'alert-success')

        else:
            print('Form is not valid')
            print(contact_form.errors)

    return render(request, 'main/contact_us.html')
