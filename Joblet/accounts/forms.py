from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Project, Education, Experince, Skill




class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  
        user.email = self.cleaned_data['email']  
        user.first_name = self.cleaned_data['first_name']  
        user.last_name = self.cleaned_data['last_name']  
        if commit:
            user.save()
        return user
    

class SignInForm(AuthenticationForm):
    pass


    

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, max_length=30, label="First Name")
    last_name = forms.CharField(required=False, max_length=30, label="Last Name")

    class Meta:
        model = Profile
        fields = ['about', 'avatar']

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.cleaned_data['first_name']:
            profile.user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data['last_name']:
            profile.user.last_name = self.cleaned_data['last_name']

        if commit:
            profile.user.save()  
            profile.save()

        return profile

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name']
    
    def __str__(self):
        return self.skill_name

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'tools_used', 'created_at']



class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['start_date', 'end_date', 'university', 'certificate']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),  
            'end_date': forms.DateInput(attrs={'type': 'date'}),    
        }

class ExperinceForm(forms.ModelForm):
    class Meta:
        model = Experince
        fields = ['start_date', 'end_date', 'company', 'position']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),  
            'end_date': forms.DateInput(attrs={'type': 'date'}),   
        }

