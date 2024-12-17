from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Match
# Create your views here.


def match_users_view(request: HttpRequest):
    matches = Match.objects.all()

    return render(request, 'main/home.html', {'matches':matches})

