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
                try:
                    active_index = int(request.GET.get('active', 0))
                    active_index = active_index % total_cards
                except ValueError:
                    active_index = 0

                prev_index = (active_index - 1) % total_cards
                next_index = (active_index + 1) % total_cards

                # Create carousel items with liked status
                for i, org in enumerate(orgs):
                    if i in [prev_index, active_index, next_index]:
                        position_class = 'active' if i == active_index else ('left' if i == prev_index else 'right')
                        # Check if org is liked by current candidate
                        is_liked = OrganizationLike.objects.get(
                            candidate=request.user.candidate,
                            organization=org
                        ).exists()

                        carousel_items.append({
                            'org': org,
                            'position_class': position_class,
                            'is_liked': is_liked
                        })

                # Profile completion check
                if not request.user.is_superuser:
                    try:
                        user_candidate = Candidate.objects.get(user=request.user)
                        if user_candidate.profile_completion <= 80:
                            messages.warning(request, 'Your profile is not complete. Please complete it to continue.', 'alert-warning')
                    except Candidate.DoesNotExist:
                        pass

            super_liked_orgs = OrganizationSuperLike.objects.filter(
                candidate=request.user.candidate
            ).values_list('organization', flat=True)

            return render(request, "main/home.html", {
                'orgs': orgs,
                'carousel_items': carousel_items,
                'total_cards': total_cards,
                'super_liked_orgs': super_liked_orgs
            })

        elif group.name == 'organizations':
            candidates = Candidate.objects.all()
            total_cards = len(candidates)
            carousel_items = []

            if total_cards > 0:
                try:
                    active_index = int(request.GET.get('active', 0))
                    active_index = active_index % total_cards
                except ValueError:
                    active_index = 0

                prev_index = (active_index - 1) % total_cards
                next_index = (active_index + 1) % total_cards

                # Create carousel items with liked status
                for i, candidate in enumerate(candidates):
                    if i in [prev_index, active_index, next_index]:
                        position_class = 'active' if i == active_index else ('left' if i == prev_index else 'right')
                        # Check if candidate is liked by current organization
                        is_liked = CandidateLike.objects.filter(
                            organization=request.user.organization,
                            candidate=candidate
                        ).exists()

                        carousel_items.append({
                            'candidate': candidate,
                            'position_class': position_class,
                            'is_liked': is_liked
                        })

                # Profile completion check
                if not request.user.is_superuser:
                    try:
                        user_org = Organization.objects.get(profile=request.user)
                        if user_org.profile_completion <= 80:
                            messages.warning(request, 'Your profile is not complete. Please complete it to continue.', 'alert-warning')
                    except Organization.DoesNotExist:
                        pass

            super_liked_cands = CandidateSuperLike.objects.filter(
                organization=request.user.organization
            ).values_list('candidate', flat=True)

            return render(request, "main/home.html", {
                'candidates': candidates,
                'carousel_items': carousel_items,
                'total_cards': total_cards,
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
