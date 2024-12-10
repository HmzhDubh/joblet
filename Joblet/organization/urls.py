from django.urls import path
from . import views

app_name = 'organization'
urlpatterns = [
    path('profile/<user_name>', views.org_profile, name='org_profile')
]