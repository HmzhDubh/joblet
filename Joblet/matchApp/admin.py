from django.contrib import admin
from .models import Match, CandidateLike, OrganizationLike, OrganizationSuperLike, CandidateSuperLike
# Register your models here.

admin.site.register(Match)
admin.site.register(CandidateLike)
admin.site.register(OrganizationLike)
admin.site.register(CandidateSuperLike)
admin.site.register(OrganizationSuperLike)