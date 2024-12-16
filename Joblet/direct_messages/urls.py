from django.urls import path
from . import views

app_name = 'direct_messages'
urlpatterns = [
    path('Dm/',views.direct_messages_view,name='direct_messages_view'),
    path('chat/<int:recipient_id>/', views.chat_view, name='chat_view'),
    path('chat/<int:recipient_id>/send/', views.send_message, name='send_message'),
]