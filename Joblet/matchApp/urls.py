from django.urls import path
from . import views

app_name = 'matchApp'

urlpatterns = [
    path('', views.match_users_view, name='match_users_view'),

]