from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import ContactForm
from organization.models import Organization
from candidate.models import Candidate

# Create your views here.


def home_view(request: HttpRequest):

    if not request.user.is_authenticated:
        return render(request, "main/home.html")

    for group in request.user.groups.all():
        if group.name == 'candidate':
            # Get all organizations
            orgs = Organization.objects.all()
            total_orgs = len(orgs)
            carousel_items = []

            if total_orgs > 0:
                # Get the current active index (could be from query params or session)
                try:
                    active_index = int(request.GET.get('active', 0))
                    # Ensure active_index is within bounds
                    active_index = active_index % total_orgs
                except ValueError:
                    active_index = 0

                # Calculate previous and next indices with wrap-around
                prev_index = (active_index - 1) % total_orgs
                next_index = (active_index + 1) % total_orgs

                # Create carousel items
                for i, org in enumerate(orgs):
                    if i in [prev_index, active_index, next_index]:
                        position_class = 'active' if i == active_index else ('left' if i == prev_index else 'right')
                        carousel_items.append({
                            'org': org,
                            'position_class': position_class
                        })

                # Profile completion check
                if not request.user.is_superuser:
                    try:
                        user_candidate = Candidate.objects.get(user=request.user)
                        if user_candidate.profile_completion <= 80:
                            messages.warning(request, 'Your profile is not complete. Please complete it to continue.', 'alert-warning')
                    except Candidate.DoesNotExist:
                        pass
            
            return render(request, "main/home.html", {
                'orgs': orgs,
                'carousel_items': carousel_items,
                'total_orgs': total_orgs,
                'total_candidates' : total_orgs
            })

        elif group.name == 'organizations':
            # Get all candidates
            candidates = Candidate.objects.all()
            total_candidates = len(candidates)
            carousel_items = []

            if total_candidates > 0:
                # Get the current active index (could be from query params or session)
                try:
                    active_index = int(request.GET.get('active', 0))
                    # Ensure active_index is within bounds
                    active_index = active_index % total_candidates
                except ValueError:
                    active_index = 0

                # Calculate previous and next indices with wrap-around
                prev_index = (active_index - 1) % total_candidates
                next_index = (active_index + 1) % total_candidates

                # Create carousel items
                for i, candidate in enumerate(candidates):
                    if i in [prev_index, active_index, next_index]:
                        position_class = 'active' if i == active_index else ('left' if i == prev_index else 'right')
                        carousel_items.append({
                            'candidate': candidate,
                            'position_class': position_class
                        })

                # Profile completion check
                if not request.user.is_superuser:
                    try:
                        user_org = Organization.objects.get(profile=request.user)
                        if user_org.profile_completion <= 80:
                            messages.warning(request, 'Your profile is not complete. Please complete it to continue.', 'alert-warning')
                    except Organization.DoesNotExist:
                        pass
            
            return render(request, "main/home.html", {
                'candidates': candidates,
                'carousel_items': carousel_items,
                'total_candidates': total_candidates
            })

    return render(request, "main/home.html")


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
