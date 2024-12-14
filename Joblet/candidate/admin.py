from django.contrib import admin
from .models import Candidate
# Register your models here.


class CandidateAdmin(admin.ModelAdmin):
    list_display = ['approved', 'profile_completion']

admin.site.register(Candidate, CandidateAdmin)