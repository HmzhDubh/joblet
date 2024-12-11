from django.urls import path
from . import views

app_name = 'direct_messages'
urlpatterns = [
    path('Dm/',views.direct_messages_view,name='direct_messages_view'),
]