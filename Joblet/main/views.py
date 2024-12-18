from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import ContactForm
from organization.models import Organization
from candidate.models import Candidate

from matchApp.models import OrganizationLike, CandidateLike, Match

from matchApp.models import OrganizationSuperLike, CandidateSuperLike
# Create your views here.


def home_view(request: HttpRequest):

    cands = Candidate.objects.all()
    orgs = Organization.objects.all()
    
    if not request.user.is_authenticated:
        return render(request, "main/home.html", context={'cands': cands, 'orgs': orgs})

    for group in request.user.groups.all():
        if group.name == 'candidate':
            # Get all organizations
            orgs = Organization.objects.all()
            total_cards = len(orgs)
            carousel_items = []

            if total_cards > 0:
                # Get the current active index (could be from query params or session)
                try:
                    active_index = int(request.GET.get('active', 0))
                    # Ensure active_index is within bounds
                    active_index = active_index % total_cards
                except ValueError:
                    active_index = 0

                # Calculate previous and next indices with wrap-around
                prev_index = (active_index - 1) % total_cards
                next_index = (active_index + 1) % total_cards

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
            liked_orgs = OrganizationLike.objects.all()
            if org in liked_orgs:
                print(True)
            else:
                print(False)
            super_liked_orgs = OrganizationSuperLike.objects.all()
            return render(request, "main/home.html", {
                'orgs': orgs,
                'carousel_items': carousel_items,
                'total_cards': total_cards,
                'liked_orgs': liked_orgs,
                'super_liked_orgs': super_liked_orgs
            })

        elif group.name == 'organizations':
            # Get all candidates
            candidates = Candidate.objects.all()
            total_cards = len(candidates)
            carousel_items = []

            if total_cards > 0:
                # Get the current active index (could be from query params or session)
                try:
                    active_index = int(request.GET.get('active', 0))
                    # Ensure active_index is within bounds
                    active_index = active_index % total_cards
                except ValueError:
                    active_index = 0

                # Calculate previous and next indices with wrap-around
                prev_index = (active_index - 1) % total_cards
                next_index = (active_index + 1) % total_cards

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
            liked_cands = CandidateLike.objects.all()
            super_liked_cands = CandidateSuperLike.objects.all()
            return render(request, "main/home.html", {
                'candidates': candidates,
                'carousel_items': carousel_items,
                'total_cards': total_cards,
                'liked_cands': liked_cands,
                'super_liked_cands': super_liked_cands
            })

    return render(request, "main/home.html", context={'cands': cands, 'orgs': orgs})


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
