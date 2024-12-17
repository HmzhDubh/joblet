from django.urls import path
from . import views

app_name = 'candidate'
urlpatterns = [
    path('profile/<user_name>/', views.candidate_profile_view, name='candidate_profile_view'),
    path('organization//update/<candidate_id>', views.change_candidate_status, name='change_candidate_status'),
    path('profile/skill/add/', views.add_skill, name='add_skill'),
    path('profile/skill/remove/<skill_id>/', views.remove_skill, name='remove_skill'),

    path('profile/project/add/', views.add_project, name='add_project'),
    path('profile/project/remove/<project_id>/', views.remove_project, name='remove_project'),

    path('profile/education/add/', views.add_education, name='add_education'),
    path('profile/education/remove/<education_id>/', views.remove_education, name='remove_education'),

    path('profile/experience/add/', views.add_experience, name='add_experience'),
    path('profile/experience/remove/<experience_id>/', views.remove_experience, name='remove_experience'),
    path('candidate/like/<org_id>', views.like_candidate, name='like_candidate'),

]