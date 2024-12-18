from django.urls import path
from . import views

app_name = 'matchApp'

urlpatterns = [
    path('candidate/<candidate_id>/super/like', views.candidate_super_like, name='candidate_super_like'),
    path('organization/<organization_id>/super/like', views.organization_super_like, name='organization_super_like'),

]