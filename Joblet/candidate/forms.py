from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from organization.models import Organization, Skill


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name']

    def __str__(self):
        return self.skill_name
