from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from matchApp.models import Match


# Create your views here.
def direct_messages_view(request:HttpRequest):
     # Get all messages involving the logged-in user
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).select_related('sender', 'recipient').order_by('timestamp')

    # Find unique users and their last message
    conversations = {}
    for message in messages:
        other_user = message.sender if message.sender != request.user else message.recipient
        if other_user not in conversations:
            conversations[other_user] = message

    # Convert dictionary to a list of tuples for the template
    conversations_list = [{'user': user, 'last_message': msg} for user, msg in conversations.items()]
    matches = Match.objects.filter(
        Q(candidate=request.user.candidate.id) | Q(organization=request.user.id)
    )
    return render(request, "direct_messages/direct_messages.html", {'conversations': conversations_list, 'matches':matches})

@login_required
def chat_view(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    messages = Message.objects.filter(
        sender=request.user, recipient=recipient) | Message.objects.filter(sender=recipient, recipient=request.user).order_by('timestamp')
    return render(request, 'direct_messages/chat.html', {'messages': messages, 'recipient': recipient})



@login_required
def send_message(request, recipient_id):
    if request.method == 'POST':
        recipient = User.objects.get(id=recipient_id)
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, recipient=recipient, content=content)
        print(recipient_id,request.user.id)
        return redirect('direct_messages:chat_view', recipient_id=recipient_id)