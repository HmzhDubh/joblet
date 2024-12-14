from django.contrib import admin
from .models import Organization, Skill
# Register your models here.

class orgAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'approved']
admin.site.register(Organization, orgAdmin)


class SkillAdmin(admin.ModelAdmin):
    list_display = ['id', 'skill_name']

admin.site.register(Skill, SkillAdmin)



