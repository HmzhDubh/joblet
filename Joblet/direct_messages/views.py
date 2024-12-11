from django.shortcuts import render
from django.http import HttpRequest,HttpResponse

# Create your views here.
def direct_messages_view(request:HttpRequest):
    return render(request,"direct_messages/direct_messages.html")