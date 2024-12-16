from django.urls import path
from . import views

app_name = 'organization'
urlpatterns = [
    path('profile/<user_name>/', views.org_profile, name='org_profile'),
    path('profile/skill/add/<skill_id>/', views.add_skill, name='add_skill'),
    path('profile/skill/remove/<skill_id>/', views.remove_skill, name='remove_skill'),
    path('profile/skill/new/', views.new_skill_view, name='new_skill_view'),
    path('organization//update/<org_id>', views.change_org_status, name='change_org_status'),
    path('add_project/', views.add_project, name='add_project'),
    path('update_project/<int:project_id>/', views.update_project, name='update_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
]