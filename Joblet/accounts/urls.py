from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('candidate/signup/', views.candidate_signup_view, name='candidate_signup_view'),
    path('organization/signup/', views.organization_signup_view, name='organization_signup_view'),
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),

]