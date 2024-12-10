from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def dashboard_view(request: HttpRequest):
    return render(request, 'dashboard/dashboard.html')