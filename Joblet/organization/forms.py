from django import forms
from .models import Projects

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'description', 'tools_used']


from django import forms
from .models import Organization

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'email', 'phone_number', 'job_title', 'description', 'location', 'website', 'linkedin', 'logo', 'skills']
